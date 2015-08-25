#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time
import os
import logging
from shutil import move

from timeFunctions import *
from settings import locks, logs, arch, records, movelog, movelock

def setupLogger():
	log = logging.getLogger("weatherstation.move")
	log.setLevel(logging.INFO)
	ch = logging.StreamHandler()
	#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	formatter = logging.Formatter('%(asctime)s:[%(levelname)s] - %(message)s')
	ch.setFormatter(formatter)
	log.addHandler(ch)
	fh = logging.FileHandler(os.path.join(logs, movelog))
	fh.setFormatter(formatter)
	log.addHandler(fh)
	return log

log = setupLogger()

checkfile=os.path.join(locks,movelock)

if not os.path.exists(checkfile):
	open(checkfile,'w').close()
if not os.path.exists(arch):
	os.mkdir(arch, 0o000755)

def mycopy(keep):
	names = os.listdir(records)
	for name in names:
		if keep in name:
			continue
		move(os.path.join(records, name), arch)

check=open(checkfile,'r')
temp=check.read()
if len(temp)<1:
	check.close()
	check=open(checkfile,'w')
	check.write(str(time.time()))
	check.flush()
	log.info("updated time since file was empty")
else:
	last=time.gmtime(float(temp))
	now=time.gmtime()
	if(prevday(last,now)):
		log.info("moving records")
		mycopy(preptime())
		check.close()
		check=open(checkfile,'w')
		check.write(str(time.time()))
		check.flush()
	else:
		log.info("records were moved today already")
check.close()
