#!/usr/bin/env python

import os
import re
import subprocess
import page
import conf
import urllib

from mod_python import util

def playURL(url):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python -u %s \'%s\' | tee -a %s' %(conf.vod, url, conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, val):
    if not os.path.exists(conf.act):
        return
    cmd = 'python -u %s \'%s\' \'%s\' | tee -a %s' %(conf.act, act, val, conf.log)
    subprocess.Popen(cmd, shell=True).communicate()

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
    w    = arg.get('w', None)
    P    = arg.get('P', None)
    V    = arg.get('V', None)

    if url:
        if re.search(r'^http', url):
            v = url
        elif re.search(r'^/', url) and os.path.isdir(url):
            d = url
        elif re.search(r'^/', url) and os.path.exists(url):
            f = url
        else:
            q = url

    if P:
        p = urllib.unquote(P)

    if V:
        v = urllib.unquote(V)

    if url:
        if re.search(r'^http', url):
            v = url
        elif re.search(r'^/', url) and os.path.isdir(url):
            d = url
        elif re.search(r'^/', url) and os.path.exists(url):
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
        page.render(req, 'panel', '<br><br><br><h1>playURL %s</h1>' %(f))

    elif v:
        playURL(v)
        page.render(req, 'panel', '<br><br><br><h1>playURL <a target=_blank href=%s>%s</a><h1>' %(v, v))

    elif w:
        page.loadword(req, w)

    elif act:
        if act == 'load' and val:
            page.render(req, val, None)
        elif act == 'update':
            os.system('touch /var/tmp/autostart_update')
            page.render(req, val, None)
        else:
            sendACT(act, val)
            page.render(req, 'panel', '<br><br><br><h1>%s %s</h1>' %(act, val or ''))
    else:
        page.render(req, 'panel', None)

    return

