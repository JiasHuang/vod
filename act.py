#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import xplay

def main():
    if len(sys.argv) >= 2:
        xplay.setAct(sys.argv[1])

if __name__ == '__main__':
    main()