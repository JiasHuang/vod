#!/usr/bin/env python

import os, re
import subprocess
import page
import json
import conf

from mod_python import util

def loadHTML(req, path):
  f = open(path, 'r')
  req.write(f.read())
  f.close()

def listDIR(req, d):
  req.write('<h1>Index of %s</h1>' %(d))
  req.write('<div style="line-height:200%;font-size:20">')
  req.write('<ul>')
  for dirName, subdirList, fileList in os.walk(d):
    for subdir in sorted(subdirList):
      if subdir[0] != '.':
        req.write('<li><img src="/icons/folder.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, subdir, subdir))
    for fname in sorted(fileList):
      if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8')):
        req.write('<li><img src="/icons/movie.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, fname, fname))
    break
  req.write('</ul>')
  req.write('</div>')

def loadURL(req, url):
    loadHTML(req, conf.webpath + 'action.html')
    req.write('<br>playURL <a target="_blank" href="%s">%s</a>' %(url, url))
    cmd = 'python -u %s \'%s\'' %(conf.vod, url)
    log = open(conf.log, 'a')
    if os.path.exists('/usr/bin/xterm'):
        subprocess.Popen(['/usr/bin/xterm', '-display', ':0', '-e', cmd], stdout=log)
    else:
        subprocess.Popen(cmd, shell=True, stdout=log)
    req.write("<br>Sent")

def sendAct(act, val):
    cmd = 'python -u %s %s %s' %(conf.act, act, val)
    log = open(conf.log, 'a')
    subprocess.Popen(cmd, shell=True, stdout=log).communicate()

def index(req):

  req.content_type = 'text/html; charset=utf-8'

  #env = os.environ.copy()
  #env['DISPLAY'] = ':0'

  arg  = util.FieldStorage(req)
  url  = arg.get('url', None)
  act  = arg.get('act', None)
  val  = arg.get('val', None)
  p    = arg.get('p', None)
  q    = arg.get('q', None)

  if act == 'load':
    loadHTML(req, conf.webpath+val+'.html')
    return

  loadHTML(req, conf.webpath+'head.html')

  if p:
    src = page.listURL(req, p)
    if src != None and src != '':
        loadURL(req, src)

  elif q:
    page.search(req, q)

  elif url:
    if re.search(r'www.eslpod.com', url):
        page.loadWord(req, url)
    elif url[0:4] == 'http':
        loadURL(req, url)
    elif url[0] == '/' and os.path.isdir(url):
        listDIR(req, url)
    elif url[0] == '/' and os.path.exists(url):
        loadURL(req, url)
    else:
        page.search(req, url)

  elif act:
    sendAct(act, val)
    loadHTML(req, conf.webpath+'action.html')

  else:
    loadHTML(req, conf.webpath+'action.html')

  loadHTML(req, conf.webpath+'tail.html')

  return

