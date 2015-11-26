#!/usr/bin/env python

import sys
import os
import re
import urllib2

def get(url, local):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    open(local, 'w').write(opener.open(url).read())

def wget(url, local):
    ua = 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'
    cmd = 'wget -U \'%s\' \'%s\' -O %s' %(ua, url, local)
    os.system(cmd)

def search_bing(q):

    url = 'https://www.bing.com/videos/search?q=%s&qft=+filterui:duration-long' %(q)
    local = 'bing.html'

    get(url, local)
    text = open(local, 'r').read()

    text = re.sub('&quot;', '', text)

    match = re.finditer(r'vrhm="{([^}]*)}"', text)

    for m in match:
        p = re.search(r'p:([^,]*)', m.group())
        t = re.search(r't:([^,]*)', m.group())
        print '\n'
        print 'bing: %s' %(t.group(1))
        print '%s' %(p.group(1))



def search_yandex(q):

    pages = [1, 2, 3]

    for p in pages:

        url = 'http://www.yandex.com/video/search?text=%s&p=%s' %(q, p)
        local = 'yandex.html'

        get(url, local)
        text = open(local, 'r').read()

        text = re.sub('<b>', '', text)
        text = re.sub('</b>', '', text)

        match = re.finditer(r'href="([^"]*)" target="_blank">([^<]*)</a></h2>', text)

        for m in match:
            print '\n'
            print 'yandex: %s' %(m.group(2))
            print '%s' %(m.group(1))


def search_google(q):

    url = 'https://www.google.com.tw/search?tbm=vid&q=%s&num=30' %(q)
    local = 'google.html'

    get(url, local)
    text = open(local, 'r').read()

    match = re.finditer(r'href="([^"]*)" [^>]*>([^<]*)</a></h3>', text)

    for m in match:
        print '\n'
        print 'google: %s' %(m.group(2))
        print '%s' %(m.group(1))


def search_video(q):
    search_google(q)
    search_bing(q)
    search_yandex(q)

if __name__ == '__main__':

    if len(sys.argv) >= 2:
        q = sys.argv[1]
    else:
        q = 'tiger'

    search_video(q)

