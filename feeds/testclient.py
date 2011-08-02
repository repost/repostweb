#! /usr/bin/env python

import feedparser
import optparse
import time
import calendar
import repost
import re

def controller():
    r = repost.Client("testclient@j.sideramota.com/reposter32","password")

    if(not r.connect()):
        print "Failed to connect"

    lasttime = 0
    while(1):
        # Let xmpppy do its thing
        r.process()
        now = time.time()
        lasttime = now
        r.sendTextPost(str(now), "Test message", "www.getrepost.com")
        time.sleep(1)

def main():
    controller()

if __name__ == '__main__':
    main()
