#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import hashlib
import timeit
import xdef
import xurl

def checkURL(url):
    site = xurl.findSite(url)
    return re.compile('(youtube|dailymotion|facebook|bilibili|vimeo|youku|openload)').search(site)

def redirectURL(url):
    if re.search(r'youku', url):
        url = re.sub('player.youku.com/embed/', 'v.youku.com/v_show/id_', url)
    return url

def parseParameters(url): 
    match = re.search(r'(.*?)&ytdl_password=(.*?)$', url)
    if match:
        url = match.group(1)
        return '--video-password ' + match.group(2)
    return None

def extractURL(url):

    print('\n[ytdl][extracURL]\n')
    print('\turl: '+url)

    url = redirectURL(url)
    arg = parseParameters(url)
    m3u8 = xdef.workdir+'list_'+hashlib.md5(url).hexdigest()+'.m3u8'

    if arg:
        print('\targ: '+arg)

    if os.path.exists(m3u8):
        print('\tret: '+m3u8)
        return m3u8

    try:
        cmd = '%s -f best -g --cookies %s %s \'%s\'' %(xdef.ytdl, xdef.cookies, arg or '', url)
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
        print('\tsec: '+str(elapsed))
    except:
        print('\tret: exception')
        return ''

    result = []
    match = re.finditer(r'^http.*', output, re.MULTILINE)
    for m in match:
        result.append(m.group(0))

    if len(result) == 0:
        print('\tret: none')
        return ''

    fd = open(m3u8, 'w')
    for vid in result:
        fd.write(vid+'\n')
    fd.close()

    print('\tret: '+m3u8)
    return m3u8

def extractURL2(url):
    lists = []
    m3u8 = extractURL(url)
    if m3u8 != '':
        fd = open(m3u8, 'r')
        for l in fd.readlines():
            lists.append(l.rstrip('\n'))
        fd.close()
    return lists

def extractSUB(url):

    if not re.search(r'youtube.com', url):
        return None

    print('\n[ytdl][extracSUB]\n')
    print('\turl: '+url)

    sub = 'sub_'+hashlib.md5(url).hexdigest()

    for files in os.listdir(xdef.workdir):
        if files.startswith(sub):
            print('\tsub: '+xdef.workdir+files)
            return files

    try:
        cmd = '%s --sub-lang=en --write-sub --skip-download -o %s%s \'%s\'' %(xdef.ytdl, xdef.workdir, sub, url)
        start_time = timeit.default_timer()
        output = subprocess.check_output(cmd, shell=True)
        elapsed = timeit.default_timer() - start_time
        print('\tsec: '+str(elapsed))
    except:
        print('\tret: exception')
        return None

    m = re.search(r'Writing video subtitles to: (.*)', output)
    if m:
        local = m.group(1)
        print('\tsub: '+local)
        return local

    return None

