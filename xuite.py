#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import datetime
import xurl
import xdef

def getKey(url, mURL):

    user = None
    m = re.search(r'm.xuite.net/vlog/(.*?)/', mURL, re.DOTALL)
    if m:
        user = m.group(1)

    if user == 'isaac.ntnu':
        return '0314'

    if user == 'derriest520':
        return '1688'

    if user == 'pao62pao62':
        date = re.search(r'<span>上傳日期：</span>(\d{4})-(\d{2})-(\d{2})', xurl.load(url))
        if date:
            yyyy, mm, dd = date.group(1), date.group(2), date.group(3)
            return mm+dd

    return None

def getSource(url):

    mURL = None
    if re.search(r'^http://vlog.xuite.net/play/', url):
        txt = xurl.load(url)
        m = re.search(r'http://m.xuite.net/vlog/([^"]*)', txt)
        if m:
            mURL = m.group(0)

    if mURL == None:
        return ''

    key = getKey(url, mURL)
    if key:
        txt = xurl.post(mURL, {'pwInput': key})
    else:
        txt = xurl.load(mURL)
    m = re.search(r'data-original="([^"]*)"', txt)
    if m:
        src = m.group(1)
        hd = re.search(r'<button id="page-video-quality" data-hdsize="([^"]*)">', txt)
        if hd:
            src = re.sub('q=360', 'q='+hd.group(1), src)
        print('\n[xuite][src]\n\n\t'+src)
        return src
    return ''

def findKey(url):

    date1 = datetime.date(2004, 1, 1)
    date2 = datetime.date(2005, 1, 1)
    day = datetime.timedelta(days=1)

    while date1 <= date2:
        mmdd = date1.strftime('%m%d')
        date1 = date1 + day
        print(mmdd)
        cmd = 'wget --post-data \'pwInput=%s\' \'%s\' -O /tmp/%s.html -q' %(mmdd, url, mmdd)
        os.system(cmd)
        if os.system('grep \'data-original\' /tmp/%s.html -q' %(mmdd)) == 0:
            print('%s (OK)' %(mmdd))
            break

def findKey2(url, start, end):
    for num in xrange(start, end):
        mmdd = '{0:04}'.format(num)
        print(mmdd)
        cmd = 'wget --post-data \'pwInput=%s\' \'%s\' -O /tmp/%s.html -q' %(mmdd, url, mmdd)
        os.system(cmd)
        if os.system('grep \'data-original\' /tmp/%s.html -q' %(mmdd)) == 0:
            print('%s (OK)' %(mmdd))
            break

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        findKey2(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        findKey(sys.argv[1])

