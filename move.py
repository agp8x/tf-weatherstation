#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import logging
from shutil import move

from timeFunctions import *
from config import settings


def setup_logger():
    log = logging.getLogger("weatherstation.move")
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s:[%(levelname)s] - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    fh = logging.FileHandler(os.path.join(settings.logs, settings.movelog))
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


log = setup_logger()

checkfile = os.path.join(settings.locks, settings.movelock)

if not os.path.exists(checkfile):
    open(checkfile, 'w').close()
if not os.path.exists(settings.arch):
    os.mkdir(settings.arch, 0o000755)


def mycopy(keep):
    names = os.listdir(settings.records)
    for name in names:
        if keep in name:
            continue
        move(os.path.join(settings.records, name), settings.arch)


check = open(checkfile, 'r')
temp = check.read()
if len(temp) < 1:
    check.close()
    check = open(checkfile, 'w')
    check.write(str(time.time()))
    check.flush()
    log.info("updated time since file was empty")
else:
    last = time.gmtime(float(temp))
    now = time.gmtime()
    if prevday(last, now):
        log.info("moving records")
        mycopy(preptime())
        check.close()
        check = open(checkfile, 'w')
        check.write(str(time.time()))
        check.flush()
    else:
        log.info("records were moved today already")
check.close()
