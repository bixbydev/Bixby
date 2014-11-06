
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

GROUP_TYPE = 'StuSchoolYOG'


new_groups_query = """SELECT new_groups.*
FROM (
SELECT dpt.sitecode DEPARTMENT_ID
, CONCAT('y', s.ABBREVIATION, '-classof-', 2027 - (dpt.unit), '-students') AS GROUP_EMAIL
, CONCAT(s.DESCRIPTION, ' Class of ', 2027 - (dpt.unit)) AS GROUP_NAME
, NULL AS GROUP_STAUTS
, 1 AS DOMAIN_ID
, gt.GROUP_TYPE
, CONCAT(s.DESCRIPTION, ' Class of ', 2027 - (dpt.unit), ' (', dpt.ABBREVIATION, ')') AS GROUP_DESCRIPTION
, dpt.unit UNIQUE_ATTRIBUTE
FROM departments AS dpt
JOIN sites AS s
	ON dpt.SITEID = s.siteid

JOIN group_types AS gt
	ON gt.GROUP_TYPE = 'StuSchoolYOG'

WHERE dpt.unit > 5
) new_groups
LEFT OUTER JOIN groups g
	ON new_groups.department_id = g.DEPARTMENT_ID
		AND new_groups.group_type = g.GROUP_TYPE
			AND new_groups.unique_attribute = g.UNIQUE_ATTRIBUTE
WHERE g.GROUP_NAME IS NULL"""



get_studentYOG_add_remove = """SELECT inn.uid
, inn.groupid new_groupid
, gv.GROUPID exit_groupid
FROM (
SELECT gu.uid
, gu.last_name
, gu.first_name
, up.DEPARTMENT_ID
, gt.GROUP_TYPEID
, g.GROUPID
FROM GOOGLE_USERS AS gu
JOIN users_py AS up
	ON gu.EXTERNAL_UID = up.external_uid
		AND gu.USER_TYPEID = up.USER_TYPEID
JOIN GROUP_TYPES AS gt
	ON gt.group_type = 'StuSchoolYOG'
JOIN GROUPS AS g
	ON up.DEPARTMENT_ID = g.DEPARTMENT_ID
		AND gt.GROUP_TYPEID = g.GROUP_TYPEID
		AND up.OU_KEY = g.UNIQUE_ATTRIBUTE
JOIN USER_TYPES AS ut
	ON gu.USER_TYPEID = ut.USER_TYPEID
WHERE ut.USER_TYPE = 'Student'
AND gu.ACCOUNT_STATUS != 5
AND gu.EXTERNAL_USERSTATUS = 0
AND up.EXTERNAL_USERSTATUS = 0
) AS inn
LEFT OUTER JOIN group_view AS gv
	ON inn.uid = gv.UID
		AND inn.group_typeid = gv.GROUP_TYPEID 
WHERE inn.groupid != gv.GROUPID OR gv.GROUPID IS NULL
-- ORDER BY inn.uid
-- LIMIT 10
"""



class StudentYOG(bixbygroups.BixbyGroups):
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
				email_permission='Owner', domain_id=domain_id, department_id=department_id,\
				unique_attribute=unique_attribute)

	def refresh_add_remove_members(self, query):
		self.cursor.execute(query)
		YOG_add_remove = self.cursor.fetchall()
		for row in YOG_add_remove:
			uid, new_groupid, exit_groupid = row
			self.add_remove_user(uid, group_id_add=new_groupid, group_id_remove=exit_groupid)



def main():
	g = StudentYOG(GROUP_TYPE)
	g.setup_new_groups(new_groups_query)
	g.refresh_add_remove_members(get_studentYOG_add_remove)


if __name__ == '__main__':
	main()


