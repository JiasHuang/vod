#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import page

def main():
    if len(sys.argv) < 2:
        return
    fd = open('output.html', 'w')
    page.page(fd, sys.argv[1])
    fd.close()
    return

if __name__ == '__main__':
    main()
