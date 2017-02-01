#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xdef
import xplay

from optparse import OptionParser

def main():

    act = None
    val = None

    parser = OptionParser()
    parser.add_option("-p", "--player", dest="player")
    (options, args) = parser.parse_args()

    if options.player:
        xdef.player = options.player

    if len(args) >= 1:
        act = args[0]

    if len(args) >= 2:
        val = args[1]

    if act:
        xplay.setAct(act, val)

    return

if __name__ == '__main__':
    main()
