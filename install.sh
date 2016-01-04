#!/bin/sh

sudo cp -vu web/* /var/www/html/

if [ ! -e vod.fifo ]; then
    mkfifo vod.fifo
fi

if [ ! -e vod.fifo ]; then
    mkfifo vod.bs.fifo
fi

chmod 666 *.fifo
