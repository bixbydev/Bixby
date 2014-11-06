
#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: sqltocsv.py

import bixbygroups
import db.mysql.base
import db.oracle.base
import time

# A little something into the camera.
GROUP_TYPE = 'StudentSection'



get_sections_from_ps = """SELECT sec.id sectionid
, sec.schoolid
, 'z'||sch.abbreviation||'-'
	||SUBSTR(tr.abbreviation, 1,2)||'-'
	||SUBSTR(t.first_name, 1, 1)||'-'
	||REGEXP_REPLACE(t.last_name, '[[:punct:][:space:]]')
	||CASE WHEN sch.high_grade > 5 THEN '-'||REGEXP_REPLACE(p.abbreviation, '(\+)', 'p') ELSE '' END GROUP_EMAIL
  
, 'z '||sch.abbreviation||' '
||SUBSTR(tr.abbreviation, 1,2)||' '
||SUBSTR(t.first_name, 1, 1)||'-'
||t.last_name
||CASE WHEN sch.high_grade > 5 THEN ' - '||REGEXP_REPLACE(p.abbreviation, '(\+)', 'p') ELSE '' END Group_Name

, sch.abbreviation||' '
  ||t.Last_Name||' '
  ||CASE WHEN sch.high_grade=5 THEN crs.course_name
    ELSE tr.name||' Period '||REGEXP_REPLACE(p.abbreviation, '(\+)', 'p') END GROUP_DESCRIPTION

, sec.termid 
, sec.teacher GROUP_OWNER
, sec.course_number
, sec.section_number
, crs.course_name

FROM sections sec
JOIN terms tr
  ON sec.termid = tr.id
    AND sec.schoolid = tr.schoolid
JOIN courses crs
  ON sec.course_number = crs.course_number
JOIN teachers t
  ON sec.teacher = t.id
JOIN period p 
  ON p.schoolid=sec.schoolid 
	AND p.year_id=SUBSTR(sec.termid, 0, 2) 
	AND p.period_number=SUBSTR(REGEXP_REPLACE(sec.expression, '[[:punct:][:alpha:]]'), 0 , 2)
JOIN schools sch
  ON sec.schoolid = sch.school_number
  
WHERE sec.termid BETWEEN '2400' AND '2410'
AND (sch.high_grade > 5
OR sec.course_number LIKE '_000'
OR sec.course_number = 'SDC01')

-- AND sch.high_grade> 5
AND sec.id NOT IN (43113, 43114)

"""

get_cc_schedule_from_ps = """SELECT id ps_id
, studentid
, sectionid
, termid
, schoolid
, dateenrolled
, dateleft
FROM cc
WHERE ABS(termid) BETWEEN 2400 AND 2410
"""





new_groups_query = """SELECT sp.SCHOOLID AS DEPARTMENT_ID
, sp.GROUP_EMAIL
, sp.GROUP_NAME
, NULL AS GROUP_STATUS
, d.DOMAIN_ID
, gt.GROUP_TYPE
, sp.GROUP_DESCRIPTION
, SECTIONID AS UNIQUE_ATTRIBUTE
-- , CONCAT(gu.GOOGLE_USERNAME, '@',d.DOMAIN_NAME) GROUP_OWNER

FROM sections_py AS sp
JOIN group_types AS gt
	ON gt.GROUP_TYPE = 'StudentSection'
JOIN google_users AS gu
	ON sp.group_owner = gu.EXTERNAL_UID
JOIN domains AS d
	ON gu.DOMAIN_ID = d.DOMAIN_ID
		AND d.PRIMARY_DOMAIN = 1
		
WHERE sp.sectionid NOT IN (SELECT UNIQUE_ATTRIBUTE FROM groups WHERE GROUP_TYPE = 'StudentSection')
AND gu.USER_TYPEID = '1'

"""

get_new_group_owners = """SELECT au.uid
, g.GROUPID

FROM sections_py AS sp
JOIN groups AS g
	ON sp.sectionid = g.UNIQUE_ATTRIBUTE
	AND g.GROUP_TYPE = 'StudentSection'
JOIN active_users AS au
	ON sp.group_owner = au.external_uid
		AND au.user_type = 'Staff'
LEFT OUTER JOIN group_members AS gm
	ON au.uid = gm.UID
	AND g.GROUPID = gm.GROUPID
	AND gm.MEMBER_TYPEID = 2
WHERE gm.uid IS NULL
-- LIMIT 5
"""



get_studentsection_add_remove = """SELECT au.uid, g.groupid, gm.groupid 
FROM studentschedule_py AS ss
JOIN active_users AS au
	ON ss.studentid = au.external_uid
	AND au.user_type = 'Student'
JOIN groups AS g
	ON ss.sectionid = g.UNIQUE_ATTRIBUTE
		AND g.GROUP_TYPE = 'StudentSection'
LEFT OUTER JOIN group_members AS gm
	ON au.uid = gm.uid
		AND g.groupid = gm.groupid
WHERE STR_TO_DATE('09/30/2014', '%m/%d/%Y') BETWEEN ss.dateenrolled AND ss.dateleft
AND gm.groupid IS NULL
"""

# groups_fields = (department_id, group_email, group_name, group_description, group_status, domain_id, group_type, unique_attribute)

get_studentsection_remove_members = """SELECT gm.UID
	, gm.GROUPID
	-- , g.UNIQUE_ATTRIBUTE
	-- , gu.EXTERNAL_UID
	-- , sec.*
FROM group_members AS gm
JOIN groups AS g
	ON gm.groupid = g.groupid
		AND g.GROUP_TYPE = 'StudentSection'
JOIN google_users AS gu
	ON gm.uid = gu.uid
JOIN user_types AS ut
	ON gu.user_typeid = ut.USER_TYPEID
		AND ut.USER_TYPE = 'Student'


LEFT OUTER JOIN (SELECT gu.UID
, sp.sectionid
, gu.EXTERNAL_UID
FROM studentschedule_py AS sp
JOIN google_users AS gu
	ON sp.studentid = gu.EXTERNAL_UID
JOIN domains d
	ON gu.DOMAIN_ID = d.DOMAIN_ID
JOIN user_types AS ut
	ON gu.USER_TYPEID = ut.USER_TYPEID
		AND ut.USER_TYPE = 'Student') AS sec
ON gm.uid = sec.uid
	AND g.unique_attribute = sec.sectionid
WHERE sec.uid IS NULL
-- LIMIT 4
"""


def copy_foreign_table(source_cursor, source_query, destination_cursor, destination_table):
	"""Selects data in a foreign source database and inserts it into a table in the destination db"""
	source_cursor.execute(source_query)
	columns_list = [i[0] for i in source_cursor.description]
	source_data = source_cursor.fetchall()
	insert = 'INSERT INTO %s \n(' %destination_table
	columns = ', '.join(columns_list) +') \n'
	values = 'VALUES ('+'%s, ' *(len(columns_list) - 1) +'%s)'
	insert_query = insert + columns + values
	print "Inserting : %s records" %source_cursor.rowcount
	destination_cursor.executemany(insert_query, source_data)







class SectionGroups(bixbygroups.BixbyGroups):
	def __init__(self, group_type):
		bixbygroups.BixbyGroups.__init__(self)
		self.grouptype = group_type

	def query_new_groups(self, query):
		self.cursor.execute(query)
		self.new_groups = self.cursor.fetchall()

	def setup_new_groups(self, query):
		self.query_new_groups(query)
		for group in self.new_groups:
			department_id,\
			 group_email,\
			  group_name,\
			   group_status,\
			    domain_id,\
			     group_type,\
			      group_description,\
			       unique_attribute = group
			self.create_new_group(group_email, group_name, group_description, group_type,\
				email_permission='Member', domain_id=domain_id, department_id=department_id,\
				unique_attribute=unique_attribute)

	def update_all_group_owners(self, query):
		self.cursor.execute(query)
		all_owners = self.cursor.fetchall()
		for owner in all_owners:
			uid, group_id = owner
			self.add_owner_to_group(uid, group_id)

			
	def refresh_add_remove_members(self, query):
		"""The query pulls additional members"""
		self.cursor.execute(query)
		YOG_add_remove = self.cursor.fetchall()
		for row in YOG_add_remove:
			uid, new_groupid, exit_groupid = row
			self.add_remove_user(uid, group_id_add=new_groupid, group_id_remove=exit_groupid)

	def remove_inactive_members(self, query):
		self.cursor.execute(query)
		section_groups_remove_members = self.cursor.fetchall()
		for row in section_groups_remove_members:
			uid, exit_groupid = row
			self.remove_user_from_group(uid, exit_groupid)



def refresh_section_groups_data():
	db.mysql.base.backup_mysql()
	# Open an Oracle Cursor
	ocon = db.oracle.base.CursorWrapper()
	ocurs = ocon.cursor
	# Open a MySQL Cursor
	mcon = db.mysql.base.CursorWrapper()
	mcurs = mcon.cursor
	# refresh the sections data (groups)
	mcurs.execute('TRUNCATE TABLE sections_py')
	copy_foreign_table(ocurs, get_sections_from_ps, mcurs, 'sections_py')

	mcurs.execute('TRUNCATE TABLE studentschedule_py')
	copy_foreign_table(ocurs, get_cc_schedule_from_ps, mcurs, 'studentschedule_py')

	mcon.close()
	ocon.close()

def main():
	refresh_section_groups_data()
	g = SectionGroups(GROUP_TYPE)
	g.setup_new_groups(new_groups_query)
	g.update_all_group_owners(get_new_group_owners)
	# The query used here will not remove users. I want to fix that BEH.
	g.refresh_add_remove_members(get_studentsection_add_remove)
	g.remove_inactive_members(get_studentsection_remove_members)


if __name__ == '__main__':
	main()


