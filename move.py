#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import os

checkfile='locks/records_moved'

def prevday(then,now):
	#ist "then" gestern (oder noch älter)?
	return ((then.tm_yday<now.tm_yday) and (then.tm_year==now.tm_year)) or ((then.tm_yday==366) and (now.tm_yday==1))
def preptime():
	now=time.localtime()
	day=now.tm_mday
	month=now.tm_mon
	year=str(now.tm_year)
	if(day<10):
		day="0"+str(day)
	else:
		day=str(day)
	if(month<10):
		month="0"+str(month)
	else:
		month=str(month)
	return month+"."+day+"."+year
	
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
		os.system("./move.sh "+preptime())
		check.close()
		check=open(checkfile,'w')
		check.write(str(time.time()))
		check.flush()
	else:
		print("today")
check.close()
