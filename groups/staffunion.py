
#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: staffunion.py


import bixbygroups

get_staffunion_add_remove = """SELECT gu.UID
, sp.STAFF_CONFERENCE AS new_groupid
, gv.GROUPID AS exit_groupid
-- , gu.ACCOUNT_STATUS
-- , gu.EXTERNAL_UID
FROM GOOGLE_USERS AS gu
JOIN USER_TYPES AS ut
	ON gu.USER_TYPEID = ut.USER_TYPEID
		AND ut.USER_TYPE = 'Staff'
JOIN STAFF_PY AS sp
	ON gu.EXTERNAL_UID = sp.STAFFID
LEFT OUTER JOIN group_view AS gv
	ON gu.UID = gv.UID
		AND gv.GROUP_TYPE = 'StaffUnion'
WHERE gu.ACCOUNT_STATUS != 5
AND gu.EXTERNAL_USERSTATUS = 0
AND (gv.GROUPID IS NULL OR gv.GROUPID != sp.STAFF_CONFERENCE)"""


def refresh_staffunion():
	bg = bixbygroups.BixbyGroups()

	bg.cursor.execute(get_staffunion_add_remove)

	staffunion_add_remove = bg.cursor.fetchall()

	for row in staffunion_add_remove:
		uid, new_groupid, exit_groupid = row

		if new_groupid:
			print 'Add user', bg.username_from_uid(uid)
			print bg._groupemail_from_groupid(new_groupid)

		if exit_groupid:
			print 'Remove user', bg.username_from_uid(uid), 'From Group:', bg._groupemail_from_groupid(exit_groupid)

		bg.add_remove_user(uid, group_id_add=new_groupid, group_id_remove=exit_groupid)