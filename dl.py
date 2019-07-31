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
    print('[url] ' + url)
    print('[flt] ' + flt)
    results = []
    for m in re.finditer(flt, xurl.load2(url, local=os.path.basename(url))):
        if re.compile(flt).groups > 0:
            link = absURL(url, m.group(1))
        else:
            link = absURL(url, m.group())
        if link not in results:
            results.append(link)
            print('\t'+link)
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
        print('[dl] '+ url)
        return None

def waitJobs(procs, options):
    while len(procs) >= int(options.jobs):
        time.sleep(1)
        for p in procs:
            if p.poll() != None:
                p.communicate()
                procs.remove(p)
                break
    return procs

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
