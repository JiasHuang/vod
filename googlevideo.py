#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def search(txt):

    src = None

    match = re.finditer(r'https://.*?.googleusercontent.com/([^"]*)', txt)
    for m in match:
        src = m.group()

    if src:
        return src

    match = re.finditer(r'https://redirector.googlevideo.com/([^"]*)', txt)
    for m in match:
        src = m.group()

    if src:
        return src

    return

