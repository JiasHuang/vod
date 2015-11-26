#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import xdef

def findSite(url):
    m = re.search(r'://([^/]*)', url);
    if m:
        return m.group(1)
    return ''

def checkURL(url):
    site = findSite(url)
    return re.compile('(youtube|videomega|dailymotion|xuite|facebook|google)').search(site)

def extractURL(url):
    cmd = '%s -g --cookies %s \'%s\'' %(xdef.ytdl, xdef.cookies, url)
    try:
        src = subprocess.check_output(cmd, shell=True).rstrip('\n')
        print '\n[ytdl][src]\n\n\t%s' %(src)
        return src
    except:
        return ''
