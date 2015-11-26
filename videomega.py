#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def getSource(txt):

    with re.search(r'http://videomega.tv/([^"]*)', txt) as m:
        print '\n[videomega]\n\n\t%s' %(m.group())
        return m.group()

    return ''


