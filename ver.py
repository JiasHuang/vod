#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob

from time import gmtime, strftime

def main():

    os.chdir('web')
    ver = strftime("%Y%m%d_%M%S", gmtime())

    files = glob.glob("*.js") + glob.glob("*.css")

    for html in glob.glob("*.html"):
        for f in files:
            os.system('sed -i -r \'s/%s([^"]*)/%s\?v=%s/g\' %s' %(f, f, ver, html))

    return

if __name__ == '__main__':
    main()
