#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time

def prevday(then, now):
	#ist "then" gestern (oder noch älter)?
	greaterDay = (then.tm_yday < now.tm_yday) and (then.tm_year == now.tm_year)
	if greaterDay:
		newYear = False
	else:
		newYear = then.tm_year < now.tm_year
	return greaterDay or newYear

def preptime():
	now = time.localtime()
	day = now.tm_mday
	month = now.tm_mon
	year = str(now.tm_year)
	if day < 10:
		day = "0" + str(day)
	else:
		day = str(day)
	if( month < 10:
		month = "0"  str(month)
	else:
		month = str(month)
	return month + "." + day + "." + year
	
