#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import xplay

def main():
    if len(sys.argv) >= 3:
        return xplay.setAct(sys.argv[1], sys.argv[2])
    if len(sys.argv) >= 2:
        return xplay.setAct(sys.argv[1], None)

if __name__ == '__main__':
    main()
