#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def concatenate(title, ftype, count):
    print '[ffmpeg] concatenate'
    locallist = open("%s.txt" %(title), "w")
    for index in range(0, count):
        local = "%s_%02d.%s" %(title, index+1, ftype)
        locallist.write("file '%s'\n" %(local.encode('utf-8')))
    locallist.close()
    cmd = "ffmpeg -f concat -i \'%s.txt\' -c copy \'%s.%s\'" %(title, title, ftype)
    os.system(cmd.encode('utf-8'))
    return 0
