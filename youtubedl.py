#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import base64
import timeit
import xdef
import xurl

def findSite(url):
    m = re.search(r'://([^/]*)', url);
    if m:
        return m.group(1)
    return ''

def checkURL(url):
    site = findSite(url)
    return re.compile('(youtube|dailymotion|facebook|google|bilibili)').search(site)

def extractURL_def(url):
    print('\n[ytdl][url]\n\n\t'+url)
    cmd = '%s -g --cookies %s \'%s\'' %(xdef.ytdl, xdef.cookies, url)
    try:
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
        print('\n[ytdl][url]\n\n\t'+str(elapsed))
    except:
        return ''

    result = []
    match = re.finditer(r'^http.*', output, re.MULTILINE)
    for m in match:
        result.append(m.group(0))

    if len(result) == 0:
        return ''
    if len(result) == 1:
        return result[0]

    m3u = xdef.workdir+'ytdl_src_'+base64.urlsafe_b64encode(url)+'.m3u'
    with open(m3u, 'w') as fd:
        for vid in result:
            fd.write(vid+'\n')

    return m3u

def extractURL_alltubedownload(url):
    src = 'https://alltubedownload.net/redirect?url=%s&format=%s' %(url, 'best[protocol^=http]')
    print('\n[ytdl][src]\n\n\t'+src)
    return src

def extractURL_keepvid(url):

    if re.search(r'youtube.com', url):
        txt = xurl.load('http://keepvid.com/?url='+url)
        m = re.search(r'<a href="([^"]*)" ([^>]*)>([^<])*</a> - <b>720p</b>', txt)
        if m:
            print '\n[keepvid][src][720p]\n\n\t%s' %(m.group(1))
            return m.group(1)

        m = re.search(r'<a href="([^"]*)" class="l"', txt)
        if m:
            print '\n[keepvid][src]\n\n\t%s' %(m.group(1))
            return m.group(1)

    return None

def extractSUB_def(url):

    if re.search(r'youtube.com', url):
        cmd = '%s --sub-lang=en --write-sub --skip-download \'%s\'' %(xdef.ytdl, url)
        txt = subprocess.check_output(cmd, shell=True)
        m = re.search(r'Writing video subtitles to: (.*)', txt)
        if m:
            print('\n[ytdl][sub]\n\n\t'+m.group(1))
            sub1 = '%s%s' %(xdef.workdir, m.group(1))
            sub2 = re.sub(' ', '_', sub1)
            os.rename(sub1, sub2)
            return sub2

    return None

def extractSUB_keepvid(url):

    if re.search(r'youtube.com', url):
        txt = xurl.load('http://keepvid.com/?mode=subs&url='+url)
        m = re.search(r'<a href="([^"]*)" ([^>]*)>([^<])*</a> - <b>English</b>', txt)
        if m:
            print '\n[keepvid][sub]\n\n\t'+m.group(1)
            local = xdef.workdir+'keepvid_sub_'+base64.urlsafe_b64encode(url)
            xurl.wget(m.group(1), local)
            return local

    return None

def extractURL(url):
    return extractURL_keepvid(url) or extractURL_def(url)

