
#!/usr/bin/python

#------------------------------------------------------------------------------
#	   Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: deletesectiongroups.py

import re
# Bixby Modules
from logger import log
# log = log.logging.getLogger('bixby') # This is so awesome!
log = log.logging.getLogger('Bixby_Log')

import google.appsclient



groupformat = [{'description': 'Zimmerman Will Period: Period 6',
'emailPermission': 'Member',
'groupId': 'zwill-y1-t-zimmerman-6@berkeley.net',
'groupName': 'ZWill Y1 T-Zimmerman 6',
'permissionPreset': 'Custom'},
{'description': 'Zimmerman Will Period: Advisory',
'emailPermission': 'Member',
'groupId': 'zwill-y1-t-zimmerman-adv@berkeley.net',
'groupName': 'ZWill Y1 T-Zimmerman Adv',
'permissionPreset': 'Custom'}]


def delete_all_section_groups():
	ac = google.appsclient.AppsClient()
	allgroups = ac.get_all_groups()
	for group in allgroups:
		if re.match("z", group['groupId']):
			#print group['groupId']
			ac.group_delete_group(group['groupId'])

		else:
			print 'Skipped Group %s' %group['groupId']



# with open('delete_groups.txt', 'wb') as delete_groups:
# 	with open('other_groups.txt', 'wb') as other_groups:
# 		for group in allgroups:
# 			# print group['groupId']
# 			if re.match("z", group['groupId']):
# 				print group['groupId']
# 				delete_groups.write(group['groupId']+'\n')
# 			else:
# 				other_groups.write(group['groupId']+'\n')




#for group in allgroups:
#  if re.match('z', group):
#print group['groupId']