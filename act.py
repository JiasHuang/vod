#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import xdef

def main():
    if len(sys.argv) >= 2:
        os.system('echo %s > %s' %(sys.argv[1], xdef.fifo))

if __name__ == '__main__':
    main()
