#!/usr/bin/python

#------------------------------------------------------------------------------
#       Copyright (C) 2011 Bradley Hilton <bradleyhilton@bradleyhilton.com>
#
#  Distributed under the terms of the GNU GENERAL PUBLIC LICENSE V3. 
#______________________________________________________________________________

# There is stuff below you may need to change. Specifically in the Oracle, MySQL, And Google Provisioning API Stuff sections.

# Filename: log.py

import time
import logging
import logging.handlers

# The old Logging Facility works beautifully!
log = logging.getLogger('Bixby_Log')
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s - %(message)s')

# Log to File/File Handler
fhandler = logging.FileHandler('Bixby.log')
fhandler.setFormatter(formatter)
log.addHandler(fhandler)

#stdout Log Handler/Log to stdout
shandler = logging.StreamHandler()
shandler.setFormatter(formatter)
log.addHandler(shandler)



# In other modules import this one
# Then add:
# import logging
# l = logging.getLogger('Bixby_Log')

# # Date in DNS Serial Format
# dnsdt = str(time.strftime('%Y%m%d%H%M%S', time.localtime()))

# beginning = '+' * 100

# log.info('Starting the Bixby Staff Refresh at %s\n%s' %(dnsdt, beginning))