#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess
import jsunpack
import xurl
import xdef

def getSource_X(url):

    txt = xurl.load(url)

    stream_url = None
    unpacked = None

    packed = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', txt)
    if packed:
        # change radix before trying to unpack, 58-61 seen in testing, 62 worked for all
        packed = re.sub(r"(.+}\('.*', *)\d+(, *\d+, *'.*?'\.split\('\|'\))", "\g<01>62\g<02>", packed.group(1))
        unpacked = jsunpack.unpack(packed)

    if unpacked:
        print '\n[videowood][unpacked]\n\n\t%s' %(unpacked)
        r = re.search('.+["\']file["\']\s*:\s*["\'](.+?/video\\\.+?)["\']', unpacked)
        if r:
            stream_url = r.group(1).replace('\\', '')

    if stream_url:
        print '\n[videowood][src]\n\n\t%s' %(stream_url)
        return stream_url

    return ''

def getSource(url):
    txt = '/tmp/videowoodtv.txt'
    xurl.get(url, txt)
    cmd = 'js %svideowoodtv.site.js %s' %(xdef.codedir, txt)
    src = subprocess.check_output(cmd, shell=True).rstrip('\n')
    return src

def search(txt):

    m = re.search(r'http://videowood.tv/([^"]*)', txt)
    if m:
        return m.group()

    return

