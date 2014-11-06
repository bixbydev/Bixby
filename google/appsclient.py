#!/usr/bin/python

#------------------------------------------------------------------------------
#  Copyright (C) 2011 - 2014 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: appsapi.py

import time

# Google Modules
import gdata.apps
import gdata.service
import gdata.apps.service
import gdata.apps.groups.service
import gdata.apps.organization.service
import gdata.apps.emailsettings.service


from logger import log
log = log.logging.getLogger('Bixby_Log') # This is so awesome!

from config import config


# Got to escape/uri encode the spaces in the Org Path.
def escape_spaces(s):
	return s.replace(' ', '%20')



class AppServiceClient(object):
	def __init__(self, connection_type):
		self.connection_type = connection_type

		if connection_type.lower() == 'staff':
			self.domain_name = config.GPrimary_Domain
			self.force_passwordchange = 'true'

		elif connection_type.lower() == 'student':
			self.domain_name = config.GStudent_Domain
			self.force_passwordchange = 'false'

		else:
			log.warn("Error: No Connection Type: %s" %connection_type)
		
		self.app_service = gdata.apps.service.AppsService(email=config.GAdmin_User,
														domain=self.domain_name,
														password=config.GAdmin_Password,
														source='BixbyClient') # Fix Client String
		self.app_service.ProgrammaticLogin()
		log.info('Connected to Google')


class AppsClient(object):
	def __init__(self):
		self.staff_connection = None
		self.student_connection = None
		self.org_connection = None
		self.group_connection = None

	def create_user(self, user_type, username, last_name, first_name, password):
		appclient = self._client(user_type)
		family_name = last_name
		given_name = first_name
		force_passwordchange = appclient.force_passwordchange # need new name BEH
		try:
			appclient.app_service.CreateUser(username, family_name, given_name, password, suspended='false'
			, quota_limit=None, password_hash_function=None, change_password=force_passwordchange)
			log.info('Created User %s' %username)
			
		except gdata.apps.service.AppsForYourDomainException, e:
			if e.error_code == 1300:
				# Entity Exists
				pass
			log.exception('Error: %d <input>: %s Reason: %s User: %s' %(e.error_code, e.invalidInput, e.reason, username))
			raise

		log.info('Created User %s' %username)

	def suspend_user(self, username, user_type):
		appclient = self._client(user_type)
		log.info('Suspending Account: %s' %username)
		appclient.app_service.SuspendUser(username)

	def restore_user(self, username, user_type):
		appclient = self._client(user_type)
		log.info('Restoring Account: %s' %username)
		appclient.app_service.RestoreUser(username)

	def modify_propper_name(self, username, first_name, last_name, user_type):
		appclient = self._client(user_type)
		entry = appclient.app_service.RetrieveUser(username)
		entry.name.family_name = last_name
		entry.name.given_name = first_name
		log.info('Changing User %s Propper Name To: %s %s' %(username, first_name, last_name))
		appclient.app_service.UpdateUser(username, entry)
		
	def modify_username(self, current_username, new_username, user_type):
		appclient = self._client(user_type)
		entry = appclient.app_service.RetrieveUser(current_username)
		entry.login.user_name = new_username
		log.info('Changing Username %s to %s' %(current_username, new_username) )
		appclient.app_service.UpdateUser(current_username, entry)
	

	def get_user_info(self, username, user_type):
		appclient = self._client(user_type)
		print appclient.force_passwordchange
		return appclient.app_service.RetrieveUser(username)


	# HERE is some OU stuff
	def get_all_ous(self):
		ouclient = self._orgclient()
		return ouclient.orgservice.RetrieveAllOrgUnits(ouclient.customer_id['customerId'])

	def list_all_ous(self):
		# Could be handy later.
		return [i['orgUnitPath'] for i in self.get_all_ous()]

	def move_userslist_to_ou(self, full_ou_path, user_list):
		if len(user_list) > 25: raise
		ouclient = self._orgclient()
		log.warn(escape_spaces(full_ou_path))
		log.warn(str(user_list))
		ouclient.orgservice.MoveUserToOrgUnit(ouclient.customer_id['customerId'], escape_spaces(full_ou_path), user_list)
		log.info('Moved: %s to OU: %s' %(user_list, full_ou_path))

	def get_ou_info(self, full_ou_path):
		ouclient = self._orgclient()
		return ouclient.orgservice.RetrieveOrgUnit(ouclient.customer_id['customerId'], escape_spaces(full_ou_path))


	# Groups Stuff	
	def group_create_group(self, group_email, group_name, description, email_permission):
		groupclient = self._groupclient() # BEH I think I'm supposed to use this object, broken?
		self.group_connection.group_service.CreateGroup(group_email, group_name, description, email_permission)
		log.info('Created Group: %s' %group_email)

	def group_delete_group(self, group_email):
		groupclient = self._groupclient() # BEH I think I'm supposed to use this object, broken?
		self.group_connection.group_service.DeleteGroup(group_email)
		log.info('Deleted Group: %s' %group_email)

	def group_add_member(self, username, group_email):
		groupclient = self._groupclient()
		self.group_connection.group_service.AddMemberToGroup(username, group_email)
		log.info('Added: %s to Group: %s' %(username, group_email))

	def group_remove_member(self, username, group_email):
		groupclient = self._groupclient()
		self.group_connection.group_service.RemoveMemberFromGroup(username, group_email)
		log.info('Removed: %s From Group: %s' %(username, group_email))

	def group_add_owner(self, username, group_email):
		groupclient = self._groupclient()
		self.group_connection.group_service.AddOwnerToGroup(username, group_email)
		log.info('Added Owner: %s to Group: %s' %(username, group_email))

	def get_all_groups(self):
		groupclient = self._groupclient()
		return self.group_connection.group_service.RetrieveAllGroups()

	def _client(self, connection_type):
		"""Create a Google Client Connection in the staff and student domain"""
		if connection_type == 'Staff':
			if not self.staff_connection:
				log.info('Opening Staff Connection')
				print 'Apps Connection Staff'
				self.staff_connection = AppServiceClient(connection_type)

			else:
				log.debug('Using Open Staff Connection')
				log.info('Sleeping')
				time.sleep(config.SLEEP_TIME_SECONDS)

			return self.staff_connection

		elif connection_type == 'Student':
			if not self.student_connection:
				log.info('Opening Student Connection')
				domain_name = config.GStudent_Domain
				force_passwordchange = 'false'

				print 'Apps Connection Student'
				self.student_connection = AppServiceClient(connection_type)

			else:
				log.debug('Sleeping | Using Open Staff Connection')
				time.sleep(config.SLEEP_TIME_SECONDS)
				
			return self.student_connection

		else:
			log.error('Nothing Doing!')
			return 'Big Fat Error'

	def _orgclient(self):
		# check for existing open connnections
		if not self.org_connection:
			log.info('Opening OrgService Connection')
			self.org_connection = OrgServiceClient()

		else:
			log.debug('Sleeping | Using Open Org Connection')
			time.sleep(config.SLEEP_TIME_SECONDS)
			
		return self.org_connection

	def _groupclient(self, domain='Staff'):
		"""For now this only creates groups in the primary domain
		Eventually it should be able to create groups in the secondary domains"""
		if not self.group_connection:
			log.info('Opening GroupService Connection')
			self.group_connection = GroupServiceClient(domain)
		else:
			log.debug('Sleeping | Using Open Group Connection')
			time.sleep(config.SLEEP_TIME_SECONDS)

		return self.group_connection



class GroupServiceClient(object):
	def __init__(self, connection_type):
		try:
			self.group_service = gdata.apps.groups.service.GroupsService(email=config.GAdmin_User
								, domain=config.GPrimary_Domain
								, password=config.GAdmin_Password)
			self.group_service.ProgrammaticLogin()

		except:
			log.exception('Connection Error: GroupService')
			raise		



class OrgServiceClient(object):
	def __init__(self):
		try:
			self.orgservice = gdata.apps.organization.service.OrganizationService(config.GAdmin_User
																							, config.GAdmin_Password
																							, config.GPrimary_Domain)
			self.orgservice.ProgrammaticLogin()
			self.customer_id = self.orgservice.RetrieveCustomerId()
		except:
			log.exception('Connection Error: OrgService')
			raise


# ac = appsclient.AppsClient()


