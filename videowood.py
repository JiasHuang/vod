#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import jsunpack

def getSource(txt):

    stream_url = None
    unpacked = None

    packed = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', txt)
    if packed:
        # change radix before trying to unpack, 58-61 seen in testing, 62 worked for all
        packed = re.sub(r"(.+}\('.*', *)\d+(, *\d+, *'.*?'\.split\('\|'\))", "\g<01>62\g<02>", packed.group(1))
        unpacked = jsunpack.unpack(packed)
        
    if unpacked:
        r = re.search('.+["\']file["\']\s*:\s*["\'](.+?/video\\\.+?)["\']', unpacked)
        if r:
            stream_url = r.group(1).replace('\\', '')

    if stream_url:
        print '\n[videowood]\n\n\t%s' %(stream_url)
        return stream_url

    return ''

