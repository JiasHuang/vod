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
    except:
        print('\tret: fail')
        return ''

    result = []
    match = re.finditer(r'^http.*', output, re.MULTILINE)
    for m in match:
        result.append(m.group(0))

    if len(result) == 0:
        print('\tret: %s (%s)' %('none', str(elapsed)))
        return ''

    fd = open(m3u8, 'w')
    for vid in result:
        fd.write(vid+'\n')
    fd.close()

    print('\tret: %s (%s)' %(m3u8, str(elapsed)))
    return m3u8

def extractSUB(url):

    print('\n[ytdl][extracSUB]\n')
    print('\turl: '+url)

    sub = 'sub_'+hashlib.md5(url).hexdigest()

    for files in os.listdir(xdef.workdir):
        if files.startswith(sub):
            print('\tsub: '+xdef.workdir+files)
            return files

    if re.search(r'youtube.com', url):
        cmd = '%s --sub-lang=en --write-sub --skip-download -o %s%s \'%s\'' %(xdef.ytdl, xdef.workdir, sub, url)
        txt = subprocess.check_output(cmd, shell=True)
        m = re.search(r'Writing video subtitles to: (.*)', txt)
        if m:
            print('\tsub: '+m.group(1))
            return m.group(1)
    return None

