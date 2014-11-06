
#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: sqltocsv.py


import db.mysql.base
import util.sqltocsv

cw = db.mysql.base.CursorWrapper()
curs = cw.cursor


# I need to figure out how to deal with tables that already have data to be kept
def populate_table(csvfile, db_table, dbcursor, paranoia=True):
	if paranoia:
		dbcursor.execute('SELECT COUNT(*) FROM SITES')
		records_exist = dbcursor.fetchone()
	else:
		records_exist = (0,)

	if records_exist[0] != 0:
		print 'Something Wrong'
	else:
		print 'preform query'
		util.sqltocsv.csv_to_sql(csvfile, db_table, dbcursor)




def main():
	print 'Running Main'
	# populate_table('first_run/SITE_SETUP_FILE.csv', 'SITES', curs)
	# populate_table('first_run/STUDENT_YOG _GROUP_SETUP_IMPORT.csv', 'GROUPS', curs, paranoia=False)

	cw.close()



if __name__ == '__main__':
	main()



