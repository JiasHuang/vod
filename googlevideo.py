#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def getSource(txt):

    m = re.search(r'https://.*?.googleusercontent.com/([^"]*)', txt)
    if m:
        return m.group()

    m = re.search(r'https://redirector.googlevideo.com/([^"]*)', txt)
    if m:
        return m.group()

    return ''


