#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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
    return re.compile('(youtube|dailymotion|facebook|google)').search(site)

def extractURL(url):
    print '\n[ytdl][url]\n\n\t%s' %(url)
    cmd = '%s -g --cookies %s \'%s\'' %(xdef.ytdl, xdef.cookies, url)
    try:
        src = subprocess.check_output(cmd, shell=True).rstrip('\n')
        print '\n[ytdl][src]\n\n\t%s' %(src)
        return src
    except:
        return ''

def extractSUB(url):

    if re.search(r'youtube.com', url):
        cmd = '%s --all-subs --skip-download \'%s\'' %(xdef.ytdl, url)
        txt = subprocess.check_output(cmd, shell=True).rstrip('\n')
        m = re.search(r'Writing video subtitles to: (.*)', txt)
        if m:
            print '\n[ytdl][sub]\n\n\t%s' %(m.group(1))
            sub = '%s%s' %(xdef.workdir, m.group(1))
            sub2 = re.sub(' ', '_', sub)
            os.rename(sub, sub2)
            return sub2

    return None