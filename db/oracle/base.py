#!/usr/bin/python

#------------------------------------------------------------------------------
#  Copyright (C) 2011 - 2014 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: base.py

import sys
from config import config

from logger import log
log = log.logging.getLogger('Bixby_Log') # This is so awesome!

# Non standard Modules
try:
	import cx_Oracle
except ImportError:
	'The Module cx_Oracle is not installed'
	sys.exit(1)

def oracle_connection_paramaters():
	"""Returns the connection string used by cx_Oracle
	Someday this may ask for the credentials"""
	log.info('Using Oracle Database: %s On Host: %s' %(config.Oracle_SID, config.Oracle_Host))
	return config.Oracle_User+'/'+config.Oracle_Password+'@'+config.Oracle_Host+'/'+config.Oracle_SID

connection_string = oracle_connection_paramaters()

class CursorWrapper(object):
	def __init__(self):
		try:
			self.connection = cx_Oracle.connect(connection_string)
			self.cursor = self.connection.cursor()
			log.info("Connected to Oracle Host: %s" %config.Oracle_Host)
		except cx_Oracle.DatabaseError, e:
			log.exception(e)


	def close(self):
		try:
			self.cursor
			self.cursor.close()
			self.connection.close()
			log.info('Oracle Connection Closed')
		except AttributeError:
			log.warn('No Oracle Cursor Open')
