
#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: schoolconference.py


import bixbygroups

GROUP_TYPE = 'SchoolConference'

get_schoolconference_add_remove = """SELECT inn.uid
, inn.groupid new_groupid
, gv.GROUPID exit_groupid

FROM ( 
SELECT gu.uid
-- , gu.last_name
-- , gu.first_name
, up.DEPARTMENT_ID
, gt.GROUP_TYPEID
, g.GROUPID
FROM GOOGLE_USERS AS gu
JOIN users_py AS up
	ON gu.EXTERNAL_UID = up.external_uid
		AND gu.USER_TYPEID = up.USER_TYPEID
JOIN GROUP_TYPES AS gt
	ON gt.group_type = 'SchoolConference'
JOIN GROUPS AS g
	ON up.DEPARTMENT_ID = g.UNIQUE_ATTRIBUTE
		AND gt.GROUP_TYPEID = g.GROUP_TYPEID

JOIN USER_TYPES AS ut
	ON gu.USER_TYPEID = ut.USER_TYPEID
WHERE ut.USER_TYPE = 'Staff'
AND gu.ACCOUNT_STATUS != 5
AND gu.EXTERNAL_USERSTATUS = 0
) AS inn
LEFT OUTER JOIN group_view AS gv
	ON inn.uid = gv.UID
		AND inn.group_typeid = gv.GROUP_TYPEID 
WHERE inn.groupid != gv.GROUPID OR gv.GROUPID IS NULL"""




def refresh_schoolconference():
	bg = bixbygroups.BixbyGroups()

	bg.cursor.execute(get_schoolconference_add_remove)

	schoolconference_add_remove = bg.cursor.fetchall()

	for row in schoolconference_add_remove:
		uid, new_groupid, exit_groupid = row

		if new_groupid:
			print 'Add user', bg.username_from_uid(uid)
			print bg._groupemail_from_groupid(new_groupid)

		if exit_groupid:
			print 'Remove user', bg.username_from_uid(uid), 'From Group:', bg._groupemail_from_groupid(exit_groupid)

		bg.add_remove_user(uid, group_id_add=new_groupid, group_id_remove=exit_groupid)
