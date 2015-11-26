#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def getSource(txt):

    m = re.search(r'http://videomega.tv/([^"]*)', txt)
    if m:
        print '\n[videomega]\n\n\t%s' %(m.group())
        return m.group()

    return ''


