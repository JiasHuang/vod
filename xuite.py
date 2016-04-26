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
    if re.search('m.xuite.net/vlog/aaa1886bbb/', url):
        return 'aaa1886bbb'
    return None

def getSource(url):
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
        cmd = 'wget --post-data \'pwInput=%s\' \'%s\' -O %s.html -q' %(mmdd, url, mmdd)
        os.system(cmd)
        if os.system('grep \'data-original\' %s.html -q' %(mmdd)) == 0:
            print '%s (OK)' %(mmdd)
            break

if __name__ == "__main__":
  findKey(sys.argv[1])


