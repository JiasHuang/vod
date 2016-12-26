#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import page

def main():
    fd = open('output.html', 'w')
    page.listURL(fd, sys.argv[1])
    fd.close()
    return

if __name__ == '__main__':
    main()
