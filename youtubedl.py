#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import base64
import xdef
import xurl

def findSite(url):
    m = re.search(r'://([^/]*)', url);
    if m:
        return m.group(1)
    return ''

def checkURL(url):
    site = findSite(url)
    return re.compile('(youtube|dailymotion|facebook|google)').search(site)

def extractURL_def(url):
    print '\n[ytdl][url]\n\n\t%s' %(url)
    cmd = '%s -g --cookies %s \'%s\'' %(xdef.ytdl, xdef.cookies, url)
    try:
        src = subprocess.check_output(cmd, shell=True).rstrip('\n')
        print '\n[ytdl][src]\n\n\t%s' %(src)
        return src
    except:
        return ''

def extractURL_alltubedownload(url):
    src = 'https://alltubedownload.net/redirect?url=%s&format=%s' %(url, 'best[protocol^=http]')
    print '\n[ytdl][src]\n\n\t%s' %(src)
    return src

def extractURL_keepvid(url):

    txt = xurl.load('http://keepvid.com/?url='+url)

    match = re.search(r'<a href="([^"]*)" ([^>]*)>([^<])*</a> - <b>720p</b>', txt)
    if match:
        src = match.group(1)
        print '\n[keepvid][src][720p]\n\n\t%s' %(src)
        return src

    match = re.search(r'<a href="([^"]*)" class="l"', txt)
    if match:
        src = match.group(1)
        print '\n[keepvid][src]\n\n\t%s' %(src)
        return src

    return None

def extractURL(url):
    return extractURL_keepvid(url)

def extractSUB_def(url):

    if re.search(r'youtube.com', url):
        cmd = '%s --sub-lang=en --write-sub --skip-download \'%s\'' %(xdef.ytdl, url)
        txt = subprocess.check_output(cmd, shell=True).rstrip('\n')
        m = re.search(r'Writing video subtitles to: (.*)', txt)
        if m:
            print '\n[ytdl][sub]\n\n\t%s' %(m.group(1))
            sub = '%s%s' %(xdef.workdir, m.group(1))
            sub2 = re.sub(' ', '_', sub)
            os.rename(sub, sub2)
            return sub2

    return None

def extractSUB_keepvid(url):

    txt = xurl.load('http://keepvid.com/?mode=subs&url='+url)

    match = re.search(r'<a href="([^"]*)" ([^>]*)>([^<])*</a> - <b>English</b>', txt)
    if match:
        src = match.group(1)
        local = xdef.workdir+'keepvid_sub_'+base64.b64encode(url)
        xurl.wget(src, local)
        print '\n[keepvid][sub]\n\n\t%s' %(local)
        return local

    return None

def extractSUB(url):
    return extractSUB_keepvid(url)
