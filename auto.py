#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

import goodtv
import xdef

def main():
    os.chdir(xdef.workdir)
    goodtv.download()
    return

if __name__ == '__main__':
    main()
