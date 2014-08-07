#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import os
from timeFunctions import *

# TODO: path from settings

checkfile='locks/records_moved'

if not os.path.exists(checkfile):
	check=open(checkfile,'w')
	check.write('')
	check.close()

log=open("logs/move.log",'a')

check=open(checkfile,'r')
temp=check.read()
if len(temp)<1:
	check.close()
	check=open(checkfile,'w')
	check.write(str(time.time()))
	check.flush()
else:
	last=time.gmtime(float(temp))
	now=time.gmtime()
	if(prevday(last,now)):
		print("move")
		log.write("moving logs... @"+time.ctime()+"\n")
		log.flush()
		if not os.path.exists("arch"):
			os.mkdir("arch")
		os.system("./move.sh "+preptime())	# TODO: replace me with: https://docs.python.org/2/library/shutil.html#module-shutil
		check.close()
		check=open(checkfile,'w')
		check.write(str(time.time()))
		check.flush()
	else:
		print("today")
check.close()
