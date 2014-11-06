#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2014 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: vars.py

import getpass

# import logging
from logger import log
log = log.logging.getLogger('Bixby_Log') # This is so awesome!

# MySQL Connection Info
MySQL_Host = "localhost"
MySQL_User = "bixby_user" # 'root'
MySQL_Password = "bixbyd3v"
MySQL_DB = "BIXBY_DB"


# # User Defined Varriables
log.warn("WARNING!! Using LIVE example.com Domain Credentials")
GAdmin_User = 'bixby@example.com'
GPrimary_Domain = 'example.com'
GAdmin_Password = 'GoogleAdminPassword'
GStudent_Domain = 'students.example.com'

#Oracle Connection Varriables (For PowerSchool Installations)
Oracle_Host = 'psdata.example.com'
Oracle_User = 'psnavigator'
# Oracle_Password = getpass.getpass('Enter Password for Oracle User %s: ' %(Oracle_User))
Oracle_Password = 'PASSWORD'
Oracle_SID = 'PSPRODDB'


# Bixby CONSTANTS
rest = 3 # Time to rest between Google API Calls (Seconds)
log.info('Using Google Domain: %s' %GPrimary_Domain)

SLEEP_TIME_SECONDS = 2.0

# Set default passwords. I'd like to look at a better way to handle this.
STAFF_PASSWORD_PREFIX = 'DefaultNewStaffPassword'
STUDENT_PASSWORD_PREFIX = 'Student'

PRIMARY_DOMAIN = 'example.com'
STUDENT_DOMAIN = 'students.example.com'

"""ACCOUNT_STATUS:
		0 = Active
		1 = New
		2 = Undefined
		3 = Manually Managed
		4 = Marked for Deletion
		5 = Deleted
		"""



