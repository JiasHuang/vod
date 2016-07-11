#!/usr/bin/env python

import os
import re
import subprocess
import page
import conf

from mod_python import util

def playURL(url):
    cmd = 'python -u %s \'%s\'' %(conf.vod, url)
    log = open(conf.log, 'a')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd], stdout=log)
    else:
        subprocess.Popen(cmd, shell=True, stdout=log)

def sendACT(act, val):
    cmd = 'python -u %s \'%s\' \'%s\'' %(conf.act, act, val)
    log = open(conf.log, 'a')
    subprocess.Popen(cmd, shell=True, stdout=log).communicate()

def index(req):

    req.content_type = 'text/html; charset=utf-8'

    arg  = util.FieldStorage(req)
    url  = arg.get('url', None)
    act  = arg.get('act', None)
    val  = arg.get('val', None)
    p    = arg.get('p', None)
    q    = arg.get('q', None)
    s    = arg.get('s', None)
    v    = arg.get('v', None)
    d    = arg.get('d', None)
    f    = arg.get('f', None)

    if url:
        if re.search(r'www.eslpod.com', url):
            page.loadWord(req, url)
            return
        elif re.search(r'^http', url):
            v = url
        elif re.search(r'^/', url) and os.path.isdir(url):
            d = url
        elif re.search(r'^/', url) and os.path.exiists(url):
            f = url
        else:
            q = url

    if p:
        page.listURL(req, p)

    elif q:
        page.search(req, q, s)

    elif d:
        page.renderDIR(req, d)

    elif f:
        playURL(f)
        page.render(req, 'panel', 'playURL: '+v)

    elif v:
        playURL(v)
        page.render(req, 'panel', '<br>playURL <a target=_blank href=%s>%s</a>' %(v, v))

    elif act and val:
        if act == 'load':
            page.render(req, val, None)
        else:
            sendACT(act, val)
            page.render(req, 'panel', '<br>%s %s' %(act, val))

    elif act:
        sendACT(act, None)
        page.render(req, 'panel', '<br>%s' %(act))

    else:
        page.render(req, 'panel', None)

    return

