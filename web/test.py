#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import page

def test_pagesearch(url):
    page.search(url)

if __name__ == '__main__':
    if (len(sys.argv)) >= 2:
        test_pagesearch(sys.argv[1])
