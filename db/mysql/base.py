#!/usr/bin/python

#------------------------------------------------------------------------------
#  Copyright (C) 2011 - 2014 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: base.py

import os
import sys
import time
from config import config


from logger import log
# import logging
log = log.logging.getLogger('Bixby_Log') # This is so awesome!


# Non standard Modules
try:
	import MySQLdb
except ImportError:
	'The Module MySQLdb is not installed'
	sys.exit(1)


# Date in DNS Serial Format
def dns_serial_date():
	"""This is not necessary REMOVE"""
	return str(time.strftime('%Y%m%d%H%M%S', time.localtime()))

def backup_mysql():
	"""Backups the DB until things get very large I am going to do this every time.
	Or until I am sure my code is good."""
	dnsdt = str(time.strftime('%Y%m%d%H%M%S', time.localtime()))
	log.info("""Creating mysqldump: BIXBY_DB_Back.'%s'.sql""" %dnsdt)
	os.system("""mysqldump -h '%s' -u '%s' -p'%s' '%s' | gzip -9 > DB_Backups/BIXBY_DB_Back.'%s'.sql.gz""" \
		%(config.MySQL_Host, config.MySQL_User, config.MySQL_Password, config.MySQL_DB, dnsdt))

def restore_mysql(db, sqlfile):
	if not os.path.exists(sqlfile):
		raise TypeError("""This is totally the wrong error because I don't know the right error""")

	log.info("Restoring DB: %s from File: %s" %(db, sqlfile))	
	os.system("""mysql -h '%s' -u '%s' -p'%s' '%s' < %s""" %(config.MySQL_Host, config.MySQL_User, config.MySQL_Password, db, sqlfile))


log.info("""Using MySQL Database: %s On Host: %s""" %(config.MySQL_DB, config.MySQL_Host))

# Class opens a connection to MySQL
class CursorWrapper(object):
	"""Wrapper to open a MySQL Connection and creates a Cursor"""
	def __init__(self, host=config.MySQL_Host,
                       user=config.MySQL_User,
                       passwd=config.MySQL_Password,
                       db=config.MySQL_DB):

		self.example = 'Testing'
		self.connection = MySQLdb.connect (host = host,
                       						user = user,
                       						passwd = passwd,
                       						db = db)
		self.cursor = self.connection.cursor()
		log.info("""Setting autocommit = \"True\"""")
		self.connection.autocommit(True)
		log.info("Connected to MySQL Host: %s Database: %s" % (host, db))

	def close(self):
		self.cursor.close()
		log.info('MySQL Cursor Closed')
		# self.connection.commit()
		self.connection.close()
		log.info('MySQL Connection Closed')
		



