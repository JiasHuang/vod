#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import base64
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

    if not url:
        print('\tret: invalid url')
        return ''

    url = redirectURL(url)
    arg = parseParameters(url)

    print('\turl: %s' %(url))

    if arg:
        print('\targ: %s' %(arg))

    cmd = '%s -f best -g --cookies %s %s \'%s\'' %(xdef.ytdl, xdef.cookies, arg or '', url)
    try:
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

    if len(result) == 1:
        print('\tret: %s (%s)' %(result[0], str(elapsed)))
        return result[0]

    m3u8 = xdef.workdir+'ytdl_src_'+base64.urlsafe_b64encode(url)+'.m3u8'
    with open(m3u8, 'w') as fd:
        for vid in result:
            fd.write(vid+'\n')

    print('\tret: %s (%s)' %(m3u8, str(elapsed)))
    return m3u8

def extractSUB(url):

    print('\n[ytdl][extracSUB]\n')

    if not url:
        print('\tret: invalid url')
        return ''

    if re.search(r'youtube.com', url):
        cmd = '%s --sub-lang=en --write-sub --skip-download \'%s\'' %(xdef.ytdl, url)
        txt = subprocess.check_output(cmd, shell=True)
        m = re.search(r'Writing video subtitles to: (.*)', txt)
        if m:
            print('\tsub: '+m.group(1))
            sub1 = '%s%s' %(xdef.workdir, m.group(1))
            sub2 = re.sub(' ', '_', sub1)
            os.rename(sub1, sub2)
            return sub2
    return None

