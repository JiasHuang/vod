#!/usr/bin/env python

import os
import re
import subprocess
import urllib

import page
import conf

from mod_python import util

def runCmd(cmd):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python %s %s' %(conf.cmd, cmd or '')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def playURL(url):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python -u %s \'%s\' | tee -a %s' %(conf.vod, url, conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, num):
    if not os.path.exists(conf.act):
        return
    cmd = 'python -u %s \'%s\' \'%s\' | tee -a %s' %(conf.act, act, num, conf.log)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getUnparsedURL(req):
    m = re.search(r'=(.*)$', req.unparsed_uri, re.DOTALL)
    if m:
        return urllib.unquote(m.group(1))
    return None

def handleCmd(cmd):
    os.system('rm -f '+conf.workdir+'vod_*')
    if cmd in ['update', 'updatedb']:
        runCmd(cmd)
    elif cmd in ['def', 'low']:
        conf.loadConf(conf.vodpath+'config/vodconf_'+cmd)
    else:
        return 'error'
    return 'success'
 
def index(req):

    req.content_type = 'text/html; charset=utf-8'

    arg  = util.FieldStorage(req)
    a    = arg.get('a', None) # action
    n    = arg.get('n', None) # number
    i    = arg.get('i', None) # input
    p    = arg.get('p', None) # page
    v    = arg.get('v', None) # video
    q    = arg.get('q', None) # query
    s    = arg.get('s', None) # search
    d    = arg.get('d', None) # directory
    f    = arg.get('f', None) # file
    c    = arg.get('c', None) # command

    if i:
        if re.search(r'^#', i):
            c = i[1:]
        elif re.search(r'^http', i):
            v = i
        elif re.search(r'^/', i) and os.path.isdir(i):
            d = i
        elif re.search(r'^/', i) and os.path.exists(i):
            f = i
        else:
            q = i

    if p:
        p = getUnparsedURL(req) or p
        page.page(req, p)

    elif q:
        page.search(req, q, s)

    elif d:
        page.renderDIR(req, d)

    elif f:
        playURL(f)
        page.render(req, 'panel', '<h1>playURL %s</h1>' %(f))

    elif v:
        v = getUnparsedURL(req) or v
        playURL(v)
        page.render(req, 'panel', '<h1>playURL <a target=_blank href=%s>%s</a><h1>' %(v, v))

    elif a:
        sendACT(a, n)
        page.render(req, 'panel', '<h1>%s %s</h1>' %(a, n or ''))

    elif c:
        page.render(req, handleCmd(c), None)

    else:
        page.render(req, 'panel', None)

    return

