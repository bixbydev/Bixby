
#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2013 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: sqltocsv.py

import csv

def csv_from_sql(query, outputfile, dbcursor, supress_header=False):
	f = open(outputfile, 'wb')
	dbcursor.execute(query)
	queryresults = dbcursor.fetchall()
	csvwriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	if not supress_header:
		csvwriter.writerow([i[0] for i in queryresults.description])
	for row in queryresults:
		csvwriter.writerow(row)
		print row
	f.close()


def csv_to_sql(csvfile, db_table, dbcursor=None):
	"""Opens a CSV file. Reads the row headers
	and generates an INSERT statement and inserts 
	rows into file. Row headers must match column names
	in the insert table."""
	with open(csvfile, 'rU') as f:
		reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		headers = reader.next()
		print headers
		data = []
		insert = 'INSERT INTO %s \n(' %db_table
		columns = ', '.join(headers) +') \n'
		values = 'VALUES ('+'%s, ' *(len(headers) - 1) +'%s)'
		query = insert + columns + values

		for row in reader:
			if dbcursor:
				dbcursor.execute(query, row)
			print query %tuple(row)

