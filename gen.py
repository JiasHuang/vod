#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import time
import threading
import xurl
import ffmpeg
import flvcn

from xml.etree import ElementTree

dl_maxthread = 0
dl_thread = []
dl_count = 0
dl_agent = 'wget'

def download(remote, local):
    if dl_agent == '':
        print('simulate %s --> %s' %(remote, local))
    elif dl_agent == 'wget':
        xurl.wget(remote, local)
    elif dl_agent == 'urlretrieve':
        xurl.urlretrieve(remote, local)

def getAliveThreadCount():
    cnt = 0
    for i in range(0, dl_count):
        t = dl_thread[i]
        if t.is_alive():
            cnt += 1
    return cnt

def getReady(local, size):
    if os.path.exists(local):
        x = os.path.getsize(local)
    else:
        x = 0
    if x and x >= size:
        return 0
    else:
        return -1

def download_RunThread(remote, local):
    global dl_thread
    global dl_count

    while (getAliveThreadCount() >= dl_maxthread):
        time.sleep(1)

    t = threading.Thread(target=download, args=(remote, local))
    t.daemon = True
    t.start()
    dl_thread.append(t)
    dl_count += 1

def download_clip_JoinThread():
    for t in dl_thread:
        t.join()

def processXML(path):

    path = os.path.abspath(path)
    obj = flvcn.genXMLObject(path)

    if not os.path.exists(obj.title):
        os.makedirs(obj.title)

    os.chdir(obj.title)

    if not os.path.exists(obj.title+'.xml'):
        shutil.copy2(path, obj.title+'.xml')

    if not os.path.exists(obj.title+".m3u"):
        playlist = open(obj.title+".m3u", "w")
        for index in range(0, obj.count):
            local = "%s_%02d.%s" %(obj.title, index+1, obj.ftype[index])
            playlist.write("%s\n" %(local.encode('utf-8')))
        playlist.close()

    for index in range(0, obj.count):
        local = "%s_%02d.%s" %(obj.title, index+1, obj.ftype[index])
        if getReady(local, obj.size[index]) == -1:
            if dl_maxthread > 1:
                download_RunThread(obj.furl[index], local)
            else:
                download(obj.furl[index], local)

    if dl_maxthread > 1:
        download_clip_JoinThread()

    readycnt = 0
    for index in range(0, obj.count):
        local = "%s_%02d.%s" %(obj.title, index+1, obj.ftype[index])
        if getReady(local, obj.size[index]) != -1:
            readycnt += 1

    if obj.count > 1 and readycnt == obj.count:
        merge = '%s.%s' %(obj.title, obj.ftype[0])
        if not os.path.exists(merge):
            ffmpeg.concatenate(obj.title, obj.ftype[0], obj.count)
        print('[gen] %s OK' %(merge))

