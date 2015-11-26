#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import gen
import os
import shutil
import time
import xurl

if __name__ == "__main__":

    url = sys.argv[1]
    local = '/tmp/temp.html'

    xurl.engine = 'Firefox'
    xurl.webdrv(url, local)
