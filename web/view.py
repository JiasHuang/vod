#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import json

import page
import conf
import xurl

from mod_python import util, Cookie

class play_obj:
    def __init__(self, video):
        self.type = 'play'
        self.video = video

class act_obj:
    def __init__(self, act='', num=''):
        self.type = 'act'
        self.act = act
        self.num = num

class cmd_obj:
    def __init__(self, status):
        self.type = 'cmd'
        self.status = status

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

def runCmd(cmd):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python %s %s' %(conf.cmd, cmd or '')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def playURL(url, opt=None):
    if not os.path.exists(conf.vod):
        return
    cmd = 'python %s \'%s\' %s' %(conf.vod, url, opt or '')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd])
    else:
        subprocess.Popen(cmd, shell=True)

def sendACT(act, num):
    if not os.path.exists(conf.act):
        return
    cmd = 'python %s \'%s\' \'%s\'' %(conf.act, act, num)
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-geometry', '80x24-50+50', '-display', ':0', '-e', cmd]).communicate()
    else:
        subprocess.Popen(cmd, shell=True).communicate()

def getCookie(req, key):
    cookies = Cookie.get_cookies(req)
    if cookies and cookies.has_key(key):
        return cookies[key].value
    return None

def getOption(req):
    fmt      = getCookie(req, 'format')
    subtitle  = getCookie(req, 'subtitle')
    pagelist = getCookie(req, 'pagelist')
    dlconf   = getCookie(req, 'dlconf')
    opt = []
    if fmt:
        opt.append('-f \'%s\'' %(fmt))
    if subtitle:
        opt.append('--subtitle \'%s\'' %(subtitle))
    if pagelist:
        opt.append('--pagelist \'%s\'' %(pagelist))
    if dlconf:
        opt.append('--dlconf \'%s\'' %(dlconf))

    return ' '.join(opt)

def handleCmd(cmd):
    cmd = cmd.lower()
    if cmd in ['update', 'updatedb']:
        os.system('rm -f '+conf.workdir+'vod_*')
        runCmd(cmd)
    else:
        return 'error'
    return 'success'

def index(req):

    req.content_type = 'text/html; charset=utf-8'
    form = req.form or util.FieldStorage(req)
    txt = '{}'

    v = search(r'view\.py\?v=(.*)$', req.unparsed_uri, re.DOTALL)

    a = form.get('a', None) # action
    n = form.get('n', None) # number
    f = form.get('f', None) # file
    c = form.get('c', None) # command

    if v:
        obj = play_obj(v)
        playURL(v, getOption(req))
        txt = json.dumps(obj.__dict__)

    elif f:
        obj = play_obj(f)
        playURL(f)
        txt = json.dumps(obj.__dict__)

    elif a:
        obj = act_obj(a, n)
        sendACT(a, n)
        txt = json.dumps(obj.__dict__)

    elif c:
        status = handleCmd(c)
        obj = cmd_obj(status)
        txt = json.dumps(obj.__dict__)

    pb_cookie = Cookie.Cookie('playbackMode', xurl.readLocal(conf.playbackMode))
    Cookie.add_cookie(req, pb_cookie)
    req.write(txt)

    return

