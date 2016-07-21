#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import meta

def loadImage(req, url):
    for i in range(1, 30):
        txt = meta.load('%s/%d' %(url, i))
        m = re.search(r'<img id="img" .*? name="img" />', txt)
        if m:
            img = re.search(r'src="([^"]*)"', m.group())
            if img:
                req.write('<li><img src=%s />\n' %(img.group(1)))
        else:
            break

