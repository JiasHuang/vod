#!/usr/bin/env python

import os, sys, re
import datetime
import xurl, xdef

def getKey(url):
    if re.search('m.xuite.net/vlog/amwkx/', url):
        return '0409'
    if re.search('m.xuite.net/vlog/isaac.ntnu/', url):
        return '0314'
    if re.search('m.xuite.net/vlog/derriest520/', url):
        return '1688'
    if re.search('m.xuite.net/vlog/polosm0429/', url):
        return '0912'
    if re.search('m.xuite.net/vlog/andy23.hsu/', url):
        return '1216'
    return None

def getSource(url):

    if re.search(r'^http://vlog.xuite.net/play/', url):
        txt = xurl.load(url)
        m = re.search(r'http://m.xuite.net/vlog/([^"]*)', txt)
        if m:
            url = m.group(0)

    os.chdir(xdef.workdir)
    key = getKey(url)
    if key:
        txt = xurl.load(url, {'pwInput': key})
    else:
        txt = xurl.load(url)
    m = re.search(r'data-original="([^"]*)"', txt)
    if m:
        print '\n[xuite][src]\n\n\t%s' %(m.group(1))
        src_sd = m.group(1)
        src_hd = re.sub('q=360', 'q=720', m.group(1))
        m3u = 'xuite.m3u'
        fd = open(m3u, 'w')
        fd.write(src_hd+'\n')
        fd.write(src_sd+'\n')
        fd.close()
        return '%s%s' %(xdef.workdir, m3u)
    return ''

def findKey(url):

    date1 = datetime.date(2004, 1, 1)
    date2 = datetime.date(2005, 1, 1)
    day = datetime.timedelta(days=1)

    while date1 <= date2:
        mmdd = date1.strftime('%m%d')
        date1 = date1 + day
        print mmdd
        cmd = 'wget --post-data \'pwInput=%s\' \'%s\' -O /tmp/%s.html -q' %(mmdd, url, mmdd)
        os.system(cmd)
        if os.system('grep \'data-original\' /tmp/%s.html -q' %(mmdd)) == 0:
            print '%s (OK)' %(mmdd)
            break

def findKey2(url, start, end):
    for num in xrange(start, end):
        mmdd = '{0:04}'.format(num)
        print mmdd
        cmd = 'wget --post-data \'pwInput=%s\' \'%s\' -O /tmp/%s.html -q' %(mmdd, url, mmdd)
        os.system(cmd)
        if os.system('grep \'data-original\' /tmp/%s.html -q' %(mmdd)) == 0:
            print '%s (OK)' %(mmdd)
            break

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        findKey2(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        findKey(sys.argv[1])

