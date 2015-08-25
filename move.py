#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import os
from shutil import move
from timeFunctions import *
from settings import locks, logs

checkfile=locks+'/records_moved'

if not os.path.exists(logs+"/move.log"):
	open(logs+"/move.log", 'w').close()
if not os.path.exists(checkfile):
	open(checkfile,'w').close()
if not os.path.exists("arch"):
	os.mkdir("arch", 0000755)

def mycopy(keep):
	names = os.listdir("records")
	for name in names:
		if keep in name:
			continue
		move(os.path.join("records", name), "arch")

log=open(logs+"/move.log",'a')

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
		mycopy(preptime())
		check.close()
		check=open(checkfile,'w')
		check.write(str(time.time()))
		check.flush()
	else:
		print("today")
check.close()
