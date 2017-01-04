#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time

import goodtv
import xdef

def countdown():
    print('tasks done, now sleeping for 10 seconds')
    for i in xrange(10, 0, -1):
        time.sleep(1)
        print(i)
    return

def main():
    os.chdir(xdef.workdir)
    goodtv.download()
    countdown()
    return

if __name__ == '__main__':
    main()
