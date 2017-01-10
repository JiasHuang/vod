#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import subprocess

import xurl
import xdef

def unpackURL(url):
    txt = xurl.load2(url)
    return unpack(txt)

def unpackFILE(local):
    txt = xurl.readLocal(local)
    return unpack(txt)

def parseCode(code):
    cnt_brace_start = 0
    cnt_brace_end = 0
    idx = 0
    func_start = 0
    func_end = 0
    for c in code:
        if c == '{':
            cnt_brace_start = cnt_brace_start + 1
            if func_start == 0:
                func_start = idx
        if c == '}':
            cnt_brace_end = cnt_brace_end + 1
            if cnt_brace_end == cnt_brace_start:
                func_end = idx
                break
        idx = idx + 1
    return code[func_start:func_end+1], code[func_end+1:-1]

def showAll(code, output):
    print('\n----------------------------------------------------- [packed] -------------------------------------------------------------\n\n')
    print(code)
    print('\n----------------------------------------------------- [unpack] -------------------------------------------------------------\n\n')
    print(output)
    print('\n----------------------------------------------------------------------------------------------------------------------------\n\n')

def unpack(txt):
    m = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', txt)
    if m:
        code = m.group()
        func, args = parseCode(code)
        local = xdef.workdir+'vod_code_'+str(os.getuid())
        if os.path.exists('/usr/bin/rhino'):
            txt = 'function unpack(p,a,c,k,e,d)%s\nprint(unpack%s);\n' %(func, args)
        else:
            txt = 'function unpack(p,a,c,k,e,d)%s\nconsole.log(unpack%s);\n' %(func, args)
        xurl.saveLocal(txt, local)
        output = subprocess.check_output('js '+local, shell=True).rstrip('\n')
        output = output.replace("\/", "/")
        showAll(code, output)
        return output
    return None

