#!/usr/bin/python

#------------------------------------------------------------------------------
#  Copyright (C) 2011 - 2014 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: bixby.py

import os
import sys
import time
import datetime
import getpass

# Bixby Modules
from logger import log
#log = log.logging.getLogger('bixby') # This is so awesome!
log = log.logging.getLogger('Bixby_Log')

import db.mysql.base
import db.oracle.base

import config.queries as queries
from config import config

import google.appsclient
import gdata.apps.service


import groups.schoolconference
import groups.staffunion
import groups.studentYOG
import groups.sectiongroups

# End Imports


class RunBixby(db.mysql.base.CursorWrapper):
	"""This class is unused and should probably be removed"""
	def __init__(self, usertype='All'):
		self.usertype = usertype
		self.bixbystart = datetime.datetime.now()
		self.mycursor = None
		self.oracursor = None


	def Finish(self):
		self.bixbyfinish = datetime.datetime.now()



class UserInfo(db.mysql.base.CursorWrapper):
	def __init__(self):
		db.mysql.base.CursorWrapper.__init__(self)

	def username_from_uid(self, uid):
		self.cursor.execute(queries.get_user_email_from_uid, (uid,))
		username = self.cursor.fetchone()
		return username[0]


class BixbyUsers(db.mysql.base.CursorWrapper, google.appsclient.AppsClient):
	def __init__(self):
		db.mysql.base.CursorWrapper.__init__(self)
		self.bixcursor = self.cursor
		google.appsclient.AppsClient.__init__(self)

	def update_username(self, current_username, new_username, usertype='Staff'):
		"""You had better be sure that the new username doesn't exist. It's not checking for that"""
		uid = self._uid_from_username(current_username, usertype)
		# I have got to move this function into this class and fix it so it just checks for unique
		# new_username = unique_username(self.bixcursor, uid)
		self.modify_username(current_username, new_username, usertype)
		self.bixcursor.execute(queries.update_google_username, (new_username, new_username, uid))
		log.info('Updated Username %s to %s' %(current_username, new_username))

	def _username_from_uid(self, uid):
		self.bixcursor.execute(queries.get_user_email_from_uid, (uid,))
		username = self.bixcursor.fetchone()
		return username[0]

	def _uid_from_username(self, username, usertype):
		self.bixcursor.execute(queries.get_uid_from_username, (username, usertype))
		uid, username = self.bixcursor.fetchone()
		return uid
	


def update_username(bixbycursor, usertype='Staff', appclient=None):
	# appclient = google.appsclient
	appclient = google.appsclient.AppsClient()
	bixbycursor.execute(queries.get_changed_username, (usertype,))
	update_username_uids = bixbycursor.fetchall()

	for uid in update_username_uids:
		uid = uid[0]
		new_username = unique_username(bixbycursor, uid)
		print 'NEW USERNAME', new_username, new_username, uid




def refresh_staff_py(oracursor, mycursor):
	"""Pulls the staff data from PowerSchool and copies it to Bixby DB
	Eventually replace this with something more system independent BEH"""
	log.info('Refreshing STAFF_PY table data')
	ps_staff = oracursor.cursor.execute(queries.get_staff_from_sis)
	ps_staff = oracursor.cursor.fetchall()
	log.info('Truncating STAFF_PY Table')
	mycursor.cursor.execute('TRUNCATE TABLE STAFF_PY')
	mycursor.cursor.executemany(queries.insert_staff_py, ps_staff)
	log.info('%s Records Inserted' %oracursor.cursor.rowcount)


def refresh_students_py(oracursor, mycursor):
	"""Pulls the student data from PowerSchool and copies it to Bixby DB
	Eventually replace this with something more system independent BEH"""
	log.info('Refreshing STUDENTS_PY table data')
	ps_students = oracursor.cursor.execute(queries.get_students_from_sis)
	ps_students = oracursor.cursor.fetchall()
	log.info('Truncating STUDENTS_PY Table')
	mycursor.cursor.execute('TRUNCATE TABLE STUDENTS_PY')
	mycursor.cursor.executemany(queries.insert_students_py, ps_students)


def multidb_bulk_insert(sourcecursor, destinationcursor, sourcequery, destinationtable):
	"""Takes two cursors connected to two different (or the same) database and creates an
	INSERT query from the source query and inserts the source data rows into the destination
	database. The column names from the source query MUST mach the column names in the
	destination table."""
	scursor = sourcecursor
	dcursor = destinationcursor
	scursor.execute(sourcequery)
	dest_col_names = [i[0] for i in scursor.description]
	dest_query_col_values = '%s, '*(len(dest_col_names) - 1) + '%s'
	dest_query_col_names = ', '.join(dest_col_names)
	srow_data = scursor.fetchall()
	dest_query = """INSERT INTO %s (%s) VALUES""" %(destinationtable, dest_query_col_names)
	dest_query = dest_query + '( %s)'
	dest_query = dest_query % dest_query_col_values
	log.info('Inserting %s Into Table: %s' %(scursor.rowcount, destinationtable) )
	log.debug(dest_query)
	dcursor.executemany(dest_query, srow_data)


# Determine if the username already exists
def user_exists(mycursor, uid, domain_id, username):
	"""Check Bixby DB for the existance of the username and return True/False"""
	mycursor.execute("""SELECT * FROM GOOGLE_USERS 
						WHERE uid != %s
							AND DOMAIN_ID = %s
							AND GOOGLE_USERNAME = %s""", (uid, domain_id, username))
	if mycursor.rowcount == 1:
		return True
	else:
		return False

def sanatize_username(username_string):
	"""Remove special charactors from usernames and truncate"""
	return username_string.translate(None, '\' -;@#$%!.,/').lower() #[:18]


# Generate an unique username within the domain!
def unique_username(mycursor, uid):
	# Check for Username Changes/Manual Username
	new_uname = None
	try_uname = None
	mycursor.execute(queries.get_user_info_from_uid, (uid,))
	first_name, last_name, middle_name, google_username, email_override_address, domain_id = mycursor.fetchone()
	if google_username == None and email_override_address != None:
		new_uname = email_override_address
	elif google_username == None:
		new_uname = sanatize_username(first_name+last_name)
	elif google_username != email_override_address:
		new_uname = email_override_address

	#Determine true/false username exists	
	userexists = user_exists(mycursor, uid, domain_id, new_uname)
	
	# Try creating a username with the middle initial
	if userexists and middle_name != None:
		log.info("Duplicate Username Avoided %s" %new_uname)
		new_uname = sanatize_username(first_name+middle_name[0]+last_name)
		userexists = user_exists(mycursor, uid, domain_id, new_uname)
	
	unique = 1
	while userexists == True:
		userexists = user_exists(mycursor, uid, domain_id, new_uname)

		try_uname = new_uname+str(unique)
		#try_uname = uname+str(unique) #I don't know what this is
		userexists = user_exists(mycursor, uid, domain_id, try_uname)
		
		unique = unique + 1
		
		log.info("Duplicate Username Avoided %s" %try_uname)
	
	if try_uname:
		new_uname = try_uname

	return new_uname


def create_new_users(mycursor, usertype=None):
	"""Takes a cursor to the Bixby DB and Staff or Student as the usertype.
	I'd like to fix this so that by default it creates all types. BEH
	The usertype thing is BROKEN BEH"""
	log.info('######## Creating New Users ########')
	mycursor.execute(queries.get_new_users, (usertype,))
	new_users = mycursor.fetchall()
	ac = google.appsclient.AppsClient()

	for user in new_users:
		uid, user_domain, user_type, first_name, last_name, external_usernumber = user
		new_username = unique_username(mycursor, uid)
		if user_type == 'Student':
			new_user_password = config.STUDENT_PASSWORD_PREFIX+external_usernumber
		else:
			new_user_password = config.STAFF_PASSWORD_PREFIX

		log.info('Creating %s User: %s (UID: %d)' %(user_type, new_username+'@'+user_domain, uid))

		try:
			ac.create_user(user_type, new_username, last_name, first_name, new_user_password)
		except gdata.apps.service.AppsForYourDomainException, e:
			if e.error_code == 1300:
				# Entity Exists
				mycursor.execute(queries.update_username, (new_username, new_user_password, 0, uid))
			log.exception('Error: %d Group: %s Reason: %s User: %s' %(e.error_code, e.invalidInput, e.reason, new_username))

		mycursor.execute(queries.update_username, (new_username, new_user_password, 2, uid)) # Mark Created and Insert Username
		time.sleep(config.SLEEP_TIME_SECONDS)


def james_brown():
	# return 'The funkiest man alive'
	return 'The funkiest man who ever lived!'


def chunks(l, n):
	"""Takes two arguments.
		a list, l
		and number, n
	Splits the list into a list of lists with n items."""
	return [l[i:i+n] for i in range(0, len(l), n)]


def update_org_units(bixbycursor, usertype=None):
	if not usertype:
		usertype = 'ALL'

	"""This function is cool! It relies heavily on the Bixby DB
	and the Org Units Schema is not so good. But this runs all updated
	AND New Org Members!
	I'd eventually like to add a Default unit in case a user doesn't fit
	into one of the existing OU's BEH"""
	ac = google.appsclient.AppsClient()
	
	bixbycursor.execute(queries.ou_new_member_count, (usertype,))
	new_ou_member_count = bixbycursor.fetchall()
	log.info('Rowcount: %s' %bixbycursor.rowcount)
	# You need to comment this before you forget how it works.
	for ou_row in new_ou_member_count:
		new_orgid, newmember_count, itterations, new_orgpath = ou_row
		log.info("New OrgID: %s Total NewMembers: %s Itterations: %s \n OrgPath: %s" %ou_row)
		bixbycursor.execute(queries.ou_new_members, (new_orgid,))
		ou_update = bixbycursor.fetchall()
		members_list = [i[2] for i in ou_update]
		#print "Member List: " + str(members_list)
		uids_list = [i[0] for i in ou_update]
		#print "UID List: " + str(uids_list)
		update_blocks = range(itterations)
		chunkyuids = chunks(uids_list, 25)
		chunkymembers = chunks(members_list, 25)
		
		for block in update_blocks:
			# String of email addresses for google
			updated_members = ', '.join(chunkymembers[block])
			
			# List of UID's being updated 
			updated_uids = chunkyuids[block]
			
			update = [(uid, new_orgid) for uid in chunkyuids[block]]
			log.info('New Org Path: %s' %new_orgpath)
			log.info("Chunky Members Block: " + str(chunkymembers[block]))

			#log.info('Org Unit: %s' %new_orgpath)
			#log.info('Moving Users %s' %updated_members)
			try:
				google_written_ou_path = ac.get_ou_info(new_orgpath)['orgUnitPath']
				ac.move_userslist_to_ou(google_written_ou_path, chunkymembers[block])
			except gdata.apps.service.AppsForYourDomainException, e:
				if e.error_code == 1301:
					log.exception(e)
					raise e 

			time.sleep(config.SLEEP_TIME_SECONDS) # Rest for a second. Make sure the response comes back
			bixbycursor.executemany(queries.ou_update_ou_members, update)
			log.info('Moved users: %s to OU: %s' %(updated_members, new_orgpath))


def BROKEN_update_org_units(bixbycursor, usertype=None):
	if not usertype:
		usertype = 'ALL'

	"""This function is cool! It relies heavily on the Bixby DB
	and the Org Units Schema is not so good. But this runs all updated
	AND New Org Members!
	I'd eventually like to add a Default unit in case a user doesn't fit
	into one of the existing OU's BEH"""
	ac = google.appsclient.AppsClient()
	bixbycursor.execute(queries.ou_new_member_count, (usertype,))
	
	new_ou_member_count = bixbycursor.fetchall()
	print bixbycursor.rowcount
	# You need to comment this before you forget how it works.
	for ou_row in new_ou_member_count:
		new_orgid, newmember_count, itterations, new_orgpath = ou_row
		bixbycursor.execute(queries.ou_new_members, (new_orgid,))
		ou_update = bixbycursor.fetchall()
		members_list = [i[2] for i in ou_update]
		uids_list = [i[0] for i in ou_update]
		update_blocks = range(itterations)
		chunkyuids = chunks(uids_list, 25)
		chunkymembers = chunks(members_list, 25)
		
		for block in update_blocks:
			# String of email addresses for google
			updated_members = ', '.join(chunkymembers[block])
			
			# List of UID's being updated 
			updated_uids = chunkyuids[block]
			
			update = [(uid, new_orgid) for uid in chunkyuids[block]]
			log.info('Org Unit: %s' %new_orgpath)
			log.info('Moving Users %s' %updated_members)
			ac.move_userslist_to_ou(new_orgpath, chunkymembers[block])
			bixbycursor.executemany(queries.ou_update_ou_members, update)
			log.info('Moved users: %s to OU: %s' %(updated_members, new_orgpath))


def suspended_users(bixbycursor, usertype=None, appclient=None):
	"""This function handles the suspended users"""
	if not usertype:
		usertype = 'NULL'

	appclient = google.appsclient.AppsClient()

	bixbycursor.execute(queries.get_suspended_users, (usertype,))
	suspended_user_list = bixbycursor.fetchall()
	for user in suspended_user_list:
		uid, username, domain, userstatus, old_ustat, suspendedaccount, old_suspend, utype = user
		# Suspend Staff
		suspend = True
		try:
			if (userstatus == 2 or suspendedaccount == 1) and utype == 'Staff':
				appclient.suspend_user(username, utype)
				log.info('Suspending %s UID: %s %s' %(utype, uid, username))

			# Suspend Students
			elif (userstatus == 0 and suspendedaccount == 1) and utype == 'Student':
				appclient.suspend_user(username, utype)
				log.info('Suspending %s UID: %s %s' %(utype, uid, username))
				# Need to add a suspend account for students who are exited. May look at date too?

			# Restore Any Un-Suspended Account
			elif userstatus == 0 and suspendedaccount == 0:
				appclient.restore_user(username, utype)
				log.info('Restoring %s UID: %s %s' %(utype, uid, username))

			else:
				suspend = False
				log.debug('Suspended %s Uesr %s %s not Suspended' %(utype, uid, username) )
				# Add check user leave date. Mark account for deletion.

			# THIS UPDATES THE RECORD if they should be suspended
			if suspend:
				bixbycursor.execute(queries.update_suspended_user, (userstatus, suspendedaccount, uid))
			else:
				log.debug('Suspended User Not Suspended')

		except gdata.apps.service.AppsForYourDomainException, e:
			if e.error_code == 1301:
				log.warn('%s User UID: %s %s Account Does Not Exist! MARKED DELETED' %(utype, uid, username))
				# This updates the record
				bixbycursor.execute(queries.update_suspended_user, (userstatus, suspendedaccount, uid))
				# This sets the account as deleted ACCOUNT_STATUS = 5 Account does not exist/deleted
				bixbycursor.execute(queries.update_account_status, (5, uid))


def update_proper_names(bixbycursor, usertype=None, appclient=None):
	log.info("""######### Updating Propper Names ########""")
	if not usertype:
		usertype = 'NULL' # There has to be a better way BEH

	appclient = google.appsclient.AppsClient()
	bixbycursor.execute(queries.get_changed_propper_name, (usertype,))
	changed_proper_names = bixbycursor.fetchall()
	for user in changed_proper_names:
		try:
			uid, username, old_lastname, new_lastname, old_firstname, new_firstname = user
			log.debug('Changing Propper Name for User: %s From: %s %s To: %s %s' %(uid, old_firstname, old_lastname, new_firstname, new_lastname))
			appclient.modify_propper_name(username, new_firstname, new_lastname, usertype)
			bixbycursor.execute(queries.update_propper_name, (new_firstname, new_lastname, uid))

		except gdata.apps.service.AppsForYourDomainException, e:
			if e.error_code == 1301:
				log.warn('User: %s Does Not Exist!' %username)
				# Mark the account deleted ACCOUNT_STATUS = 5 Account does not exist/deleted
				bixbycursor.execute(queries.update_account_status, (5, uid))






def staff():
	"""This function has been replaced in favor of the unified() function."""
	# Open some cursors to the DB
	m = db.mysql.base.CursorWrapper()
	o = db.oracle.base.CursorWrapper()

	# Refresh Staff from PS
	# refresh_staff_py(o, m)
	log.info('Inserting New Staff Records')
	m.cursor.execute(queries.insert_bulk_new_staff_accounts)
	log.info('Inserted %s New Staff' %m.cursor.rowcount)

	# Using the Multi-Database Bulk Insert Method (This may be really handy at some point)
	# multidb_bulk_insert(m.cursor, m.cursor, queries.get_new_staff_accounts, 'GOOGLE_USERS')

	create_new_users(m.cursor, 'Staff')

	m.close()
	o.close()


def students():
	"""This function has been replaced in favor of the unified() function."""
	# Open some cursors to the DB
	m = db.mysql.base.CursorWrapper()
	o = db.oracle.base.CursorWrapper()

	# refresh_students_py(o, m)
	log.info('Inserting New Student Records')
	m.cursor.execute(queries.insert_bulk_new_student_accounts)
	log.info('Inserted %s New Students' %m.cursor.rowcount)

	create_new_users(m.cursor, 'Student')

	m.close()
	o.close()


def refreshall():
	"""A wrapper function to refresh students and staff. 
	This is lazy"""
	# Open some cursors to the DB
	m = db.mysql.base.CursorWrapper()
	o = db.oracle.base.CursorWrapper()

	refresh_students_py(o, m)
	refresh_staff_py(o, m)

	m.close()
	o.close()


def unified():
	"""A wrapper function to run students and staff account creation."""
	# Open some cursors to the DB
	m = db.mysql.base.CursorWrapper()

	# refresh_students_py(o, m)
	log.info('Inserting New User Records')
	m.cursor.execute(queries.insert_bulk_new_user_accounts)
	# log.info('Inserted %s New Students' %m.cursor.rowcount)

	# fix this so that all or one can be run
	create_new_users(m.cursor)
	
	suspended_users(m.cursor)
	update_org_units(m.cursor, usertype='Staff')
	update_org_units(m.cursor, usertype='Student')
	update_proper_names(m.cursor, usertype='Staff')
	# update_proper_names(m.cursor, usertype='Student')

	log.info('Running Group Refresh')
	log.info('Running Staff School Conferences')
	groups.schoolconference.refresh_schoolconference()
	log.info('Running Staff Union')
	groups.staffunion.refresh_staffunion()
	log.info('Running Student YOG Groups')
	groups.studentYOG.main()
	log.info('Running Student Section Groups')
	groups.sectiongroups.main()

	m.close()



def main():
	# Backup MySQL DB
	db.mysql.base.backup_mysql()

	refreshall()
	unified()
	#staff()
	#students()




if __name__ == '__main__':
	log.info('-- Bixby Started --')
	main()
	log.info('-- Bixby Exited --')

""" Still need to deal with:
"""
