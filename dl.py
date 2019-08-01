#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import urlparse
import time

import xurl
import xsrc

from optparse import OptionParser

def absURL(ref, target):
    if target.startswith('http'):
        return target
    o = urlparse.urlparse(ref)
    if target.startswith('//'):
        return '%s:%s' %(parsed.scheme, target)
    if target.startswith('/'):
        return '%s://%s%s' %(o.scheme, o.netloc, target)
    return '%s://%s%s/%s' %(o.scheme, o.netloc, os.path.dirname(o.path) or '', target)

def filter(url, flt):
    results = []
    for m in re.finditer(flt, xurl.load2(url, local=os.path.basename(url))):
        if re.compile(flt).groups > 0:
            link = absURL(url, m.group(1))
        else:
            link = absURL(url, m.group())
        if link not in results:
            results.append(link)
    return results

def genName(name, suffix, sn):
    i = int(sn)
    while os.path.exists("%s_%03d.%s" %(name , i, suffix)):
        i += 1
    return '%s_%03d.%s' %(name, i, suffix)

def dl(url, options):
    if options.execute == 'ytdl':
        cmd = 'youtube-dl \'%s\'' %(url)
        return subprocess.Popen(cmd, shell=True)
    elif options.execute == 'ffmpeg':
        src, cookie, ref = xsrc.getSource(url)
        local = genName(options.name, options.type, options.sn)
        cmd = 'ffmpeg -i \'%s\' -vcodec copy -acodec copy %s' %(src, local)
        return subprocess.Popen(cmd, shell=True)
    elif options.cmd is not None:
        cmd = '%s \'%s\'' %(options.cmd, url)
        return subprocess.Popen(cmd, shell=True)
    else:
        return None

def waitJobs(procs, options):
    while len(procs) >= int(options.jobs):
        time.sleep(0.1)
        for p in procs:
            if p.poll() != None:
                p.communicate()
                procs.remove(p)
                break
    return procs

def getM3U8Stat(local):
    dls = 0
    dlsz = 0
    files = 0
    dldir = os.path.dirname(local)
    for m in re.finditer(r'#EXTINF:.*?\n(.*?)\n', xurl.readLocal(local)):
        f = os.path.join(dldir, m.group(1))
        if os.path.exists(f):
            dls += 1
            dlsz += os.path.getsize(f)
        files += 1
    return dls, dlsz, files

def waitM3U8Ready(local, min_dls = 4, min_dlsz = 10485760, verbose = False):
    while True:
        dls, dlsz, files = getM3U8Stat(local)
        if files > 0 and dls == files:
            break
        if dls > min_dls or dlsz > min_dlsz:
            break
        if verbose:
            print('waiting jobs ... (dls %s/%s dlsz %s)' %(dls, files, dlsz))
        time.sleep(2)

def createJobs(url, dldir, jobs):
    prog = os.path.realpath(__file__)
    local = dldir + os.path.basename(url)

    procs = subprocess.check_output('ps aux', shell=True)
    pattern = '%s -i %s' %(os.path.basename(prog), url)
    if re.search(re.escape(pattern), procs):
        return local

    ctx = xurl.getContentType(url)
    if ctx == 'application/vnd.apple.mpegurl' or ctx == 'application/x-mpegurl':
        flt = '#EXTINF:.*?\n(.*?)\n'
        cmd = '%s -i \'%s\' -c %s -f \'%s\' -j %s --cmd \'wget -qc -o /dev/null\'' %(
                prog, url, dldir, flt, jobs)
        p = subprocess.Popen(cmd, shell=True)
        print('create download process %s' %(p.pid))
        waitM3U8Ready(local, verbose = True)
        return local

    print('createJobs fail')
    return None

def main():

    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", action='append')
    parser.add_option("-c", "--chdir", dest="chdir")
    parser.add_option("-f", "--filter", dest="filter", action='append')
    parser.add_option("-s", "--sort", dest="sort", action='append')
    parser.add_option("-x", "--execute", dest="execute")
    parser.add_option("-j", "--jobs", dest="jobs", default='1')
    parser.add_option("-n", "--name", dest="name", default='dl')
    parser.add_option("-t", "--type", dest="type", default='mp4')
    parser.add_option("--sn", dest="sn", default='1')
    parser.add_option("--cmd", dest="cmd")
    (options, args) = parser.parse_args()

    if options.chdir:
        os.chdir(options.chdir)

    results = options.input
    results_next = []
    procs = []
    for i in range(len(options.filter)):
        for x in results:
            results_next.extend(filter(x, options.filter[i]))
        if options.sort and str(i) in options.sort:
            results_next.sort()
        results = results_next
        results_next = []

    for x in results:
        p = dl(x, options)
        if p:
            procs.append(p)
            procs = waitJobs(procs, options)

    for p in procs:
        p.communicate()

    return

if __name__ == '__main__':
    main()
