#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def getSource(txt):

    with re.search(r'https://.*?.googleusercontent.com/([^"]*)', txt) as m:
        return m.group()

    with re.search(r'https://redirector.googlevideo.com/([^"]*)', txt) as m:
        return m.group()

    return ''


