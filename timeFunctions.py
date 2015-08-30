#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import time


def prevday(then, now):
    # ist "then" gestern (oder noch älter)?
    greater_day = (then.tm_yday < now.tm_yday) and (then.tm_year == now.tm_year)
    if greater_day:
        new_year = False
    else:
        new_year = then.tm_year < now.tm_year
    return greater_day or new_year


def preptime():
    now = time.localtime()
    day = now.tm_mday
    month = now.tm_mon
    year = str(now.tm_year)
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    return month + "." + day + "." + year
