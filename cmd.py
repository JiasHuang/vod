#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

import xurl

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def loadLocal(url):
    return xurl.load2('http://127.0.0.1/vod/'+url)

def update():
    localdir = '/tmp/vodlatest'
    if os.path.exists(localdir):
        os.system('git -C %s pull' %(localdir))
    else:
        os.system('git clone http://github.com/jiashuang/vod '+localdir)
    os.system('python -m compileall '+localdir)
    os.system('sudo %s/install.sh' %(localdir))
    os.system('sudo %s/sync.sh' %(localdir))
    return

def updateDataBaseEntry(fd, url, title0):
    for m in re.finditer(r'<a href="([^"]*)">(.*?)</a>', loadLocal(url), re.DOTALL|re.MULTILINE):
        link = m.group(1)
        title = search(r'<h2>(.*?)</h2>', m.group(2))
        image = search(r'src="([^"]*)"', m.group(2))
        fd.write('<a href="%s">\n' %(link))
        fd.write('<h2>%s</h2>\n' %(title0+'/'+title))
        if image:
            fd.write('<img src="%s" />\n' %(image))
        fd.write('</a>\n')

def updatedb():
    local = os.path.expanduser('~')+'/.voddatabase'
    fd = open(local, 'w')
    for m in re.finditer(r'<a href=([^>]*)>(.*?)</a>', loadLocal('bookmark.html')):
        updateDataBaseEntry(fd, m.group(1), m.group(2))
    fd.close()

def main():

    if len(sys.argv) < 2:
        return

    cmd = sys.argv[1]

    if cmd == 'update':
        update()
    elif cmd == 'updatedb':
        updatedb()

    return

if __name__ == '__main__':
    main()
