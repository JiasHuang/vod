#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

import xdef
import xurl

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def loadLocal(url):
    return xurl.load2('http://127.0.0.1/vod/'+url)

def update():
    os.chdir('/opt/vod')
    os.system('sudo git pull')
    os.system('sudo ./install.sh')
    os.system('sudo ./sync.sh')
    return

def updateDataBaseEntry(fd, url, title0):
    for m in re.finditer(r'<a href="([^"]*)">(.*?)</a>', loadLocal(url), re.DOTALL|re.MULTILINE):
        link = m.group(1)
        title = search(r'<h2>(.*?)</h2>', m.group(2))
        image = search(r'src="([^"]*)"', m.group(2))
        fd.write('\n')
        fd.write('<a href="%s">\n' %(link))
        fd.write('<h2>%s</h2>\n' %(title0+'/'+title))
        if image:
            fd.write('<img src="%s" />\n' %(image))
        fd.write('</a>\n')

def updateDataBase():
    local = xdef.workdir+'database_'+str(os.getuid())
    fd = open(local, 'w')
    for m in re.finditer(r'<a href=([^>]*)>(.*?)</a>', loadLocal('bookmark.html')):
        updateDataBaseEntry(fd, m.group(1), m.group(2))
    fd.close()
    os.system('sudo cp %s /var/www/html/vod/database' %(local))

def main():

    if len(sys.argv) < 2:
        return

    cmd = sys.argv[1]

    if cmd == 'update':
        update()
    elif cmd == 'updateDataBase':
        updateDataBase()

    return

if __name__ == '__main__':
    main()
