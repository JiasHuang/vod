#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

import page
import meta

def main():

    if len(sys.argv) < 2:
        return

    fd = open('output.html', 'w')

    m = re.search(r'load.py\?(.*?)$', sys.argv[1])
    if m:
        q = meta.search(r'q=([^&]*)', m.group(1))
        s = meta.search(r's=([^&]*)', m.group(1))
        x = meta.search(r'x=([^&]*)', m.group(1))
        p = meta.search(r'p=([^&]*)', m.group(1))
        if q:
            page.search(fd, q, s, x)
        if p:
            page.page_core(fd, p)
    else:
        page.page(fd, sys.argv[1])

    fd.close()
    return

if __name__ == '__main__':
    main()
