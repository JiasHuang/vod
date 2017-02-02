#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

def checkProcessRunning(process):
    cmd = 'pidof %s' %(process)
    try:
        result = subprocess.check_output(cmd, shell=True)
        return result
    except:
        return None

def checkOutput(cmd, patten=None):
    output = subprocess.check_output(cmd, shell=True)
    if patten:
        m = re.search(patten, output)
        if m:
            return m.group(1)
        else:
            return None
    return output
