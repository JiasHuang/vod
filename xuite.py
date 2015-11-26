#!/usr/bin/env python

import os, sys, re
import datetime
import xurl

def getKey(url):
    if re.search('m.xuite.net/vlog/amwkx/', url):
        return '0409'
    if re.search('m.xuite.net/vlog/isaac.ntnu/', url):
        return '0314'
    return None

def getSource(url):
    key = getKey(url)
    if key:
        txt = xurl.load(url, {'pwInput': key})
    else:
        txt = xurl.load(url)
    with re.search(r'data-original="([^"]*)"', txt) as m:
        print '\n[xuite][src]\n\n\t%s' %(m.group(1))
        return re.sub('q=360', 'q=720', m.group(1))
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


