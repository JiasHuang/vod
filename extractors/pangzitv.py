#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64

import xurl

VALID_URL = r'pangzitv\.com'

def getSource(url, fmt, ref):
    if re.search(r'vod-play-id', url):
        try:
            m = re.search(r'num-(\d+)', url)
            ep_num = m.group(1)
            txt = xurl.curl(url)
            m = re.search(r'base64decode\(\'([^\']*)', txt)
            code = m.group(1)
            decoded = xurl.unquote(base64.b64decode(code))
            print('\n[pangzitv][DBG][decoded]\n\n\t%s' %(decoded))
            # process unicode special character
            decoded = decoded.replace('%u','\\u').decode('unicode_escape')
            for m in re.finditer(r'(\d+).*?(http[^#$\n]*)', decoded):
                if (int(m.group(1)) == int(ep_num)):
                    return m.group(2)
            m = re.search(r'(http[^#$\n]*)', decoded)
            if m:
                return m.group(1)
        except:
            print('Exception')
    return None

