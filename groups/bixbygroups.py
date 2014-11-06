
#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: bixbygroups.py

# Bixby Modules
from logger import log
#log = log.logging.getLogger('bixby') # This is so awesome!
log = log.logging.getLogger('Bixby_Log')

import db.mysql.base
import google.appsclient
import gdata.apps.service
import config.queries as queries
import config.config as config


class UserInfo(db.mysql.base.CursorWrapper):
	"""A class to get userinfo from the Bixby DB
	Move this to a user class BEH"""
	def __init__(self):
		db.mysql.base.CursorWrapper.__init__(self)

	def username_from_uid(self, uid):
		self.cursor.execute(queries.get_user_email_from_uid, (uid,))
		username = self.cursor.fetchone()
		return username[0]



class BixbyGroups(UserInfo, google.appsclient.AppsClient):
	def __init__(self):
		UserInfo.__init__(self)
		google.appsclient.AppsClient.__init__(self)

	def create_new_group(self, group_email, group_name, group_description, group_type, \
						group_status=1, email_permission='Owner', domain_id=1, department_id=None,\
						unique_attribute=None):
		
		"""department_id, group_email, group_name, group_description, group_status
		, domain_id, group_type, unique_attribute

		PERMISSION_OWNER = 'Owner'
		PERMISSION_MEMBER = 'Member'
		PERMISSION_DOMAIN = 'Domain'
		PERMISSION_ANYONE = 'Anyone'
		"""
		groups_fields = (department_id, group_email, group_name, group_description, group_status, domain_id, group_type, unique_attribute)
		try:
			self.group_create_group(group_email, group_name, group_description, email_permission=email_permission)
		except gdata.apps.service.AppsForYourDomainException, e:
			if e.error_code == 1300:
				log.exception(e)
				log.warn("""The Group: %s Exists. It's OK that happens.""" %group_email)
			else:
				raise e

		self.cursor.execute(queries.insert_new_group, groups_fields )
		log.info('Created Group: %s' %group_email)

	def delete_group(self, group_email):
		log.warn('Deleting Group: %s' %group_email)
		group_id = self._groupid_from_groupemail(group_email)
		
		try:
			# Delete Group from Google
			self.group_delete_group(group_email)
			
		except Exception, e: 
			if e.error_code == 1301:
				log.exception(e)
				# Entity Exists

			else:
				log.exception(e)
				raise e
		log.info('Deleting Group From DB: %s' %group_email)
		self.cursor.execute(queries.delete_group_from_groups, (group_id,))


	def add_user_to_group(self, uid, group_id):
		# Some of this stuff should probably be in a seprate class. Like the SQL BEH
		username = self.username_from_uid(uid)
		group_email = self._groupemail_from_groupid(group_id)
		self.group_add_member(username, group_email)
		self.cursor.execute('INSERT INTO GROUP_MEMBERS (UID, GROUPID, MEMBER_TYPEID) VALUES (%s, %s, %s)', (uid, group_id, 1))
		log.info('Added: %s to Group: %s' %(username, group_email))


	def remove_user_from_group(self, uid, group_id):
		username = self.username_from_uid(uid)
		group_email = self._groupemail_from_groupid(group_id)
		try:
			self.group_remove_member(username, group_email)
		except Exception, e:
			log.exception(e)
			if e.error_code == 1301:
				pass

			else:
				raise e

		self.cursor.execute("""DELETE FROM GROUP_MEMBERS 
							WHERE UID = %s 
							AND GROUPID = %s 
							-- AND MEMBER_TYPEID = 1
							""", (uid, group_id))
		log.info('Removed: %s from Group: %s' %(username, group_email))


	def add_remove_user(self, uid, group_id_add=None, group_id_remove=None):
		if group_id_remove:
			self.remove_user_from_group(uid, group_id_remove)

		if group_id_add:
			self.add_user_to_group(uid, group_id_add)


	def add_owner_to_group(self, uid, group_id):
		"""Takes the bixby uid and bixby groupid. These are the internal ids from the DB"""
		username = self.username_from_uid(uid)
		group_email = self._groupemail_from_groupid(group_id)
		# The owner needs to be a member
		self.add_user_to_group(uid, group_id)
		self.group_add_owner(username, group_email)
		self.cursor.execute('INSERT INTO GROUP_MEMBERS (UID, GROUPID, MEMBER_TYPEID) VALUES (%s, %s, %s)', (uid, group_id, 2))
		log.info('Added Owner: %s to Group: %s' %(username, group_email))





	def _groupemail_from_groupid(self, group_id):
		self.cursor.execute(queries.get_group_email_from_id, (group_id,))
		group_email = self.cursor.fetchone()
		return group_email[0]


	def _groupid_from_groupemail(self, group_email):
		self.cursor.execute(queries.get_groupid_from_groupemail, (group_email,))
		groupid = self.cursor.fetchone()
		if not groupid:
			raise TypeError('Group Does Not Exist in Bixby')
			# It should check in google. Then raise if it doesn't exist.
		else:
			return groupid[0]


	def groupinfo(self, group_email, group_name, group_description, group_id=None):
		self.group_email = group_email
		self.group_name = group_name
		self.group_description = group_description
		self.group_id = group_id






