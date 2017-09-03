#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob

from time import gmtime, strftime

def main():

    '''
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="keypad.css">

    <script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>
    <script type="text/javascript" src="panel.js"></script>
    <script type="text/javascript" src="speech.js"></script>

    '''

    os.chdir('web')
    ver = strftime("%Y%m%d", gmtime())

    for html in glob.glob("*.html"):

        for js in glob.glob("*.js"):
            os.system('sed -i -r \'s/%s([^"]*)/%s\?v=%s/g\' %s' %(js, js, ver, html))

        for css in glob.glob("*.css"):
            os.system('sed -i -r \'s/%s([^"]*)/%s\?v=%s/g\' %s' %(css, css, ver, html))

    return

if __name__ == '__main__':
    main()
