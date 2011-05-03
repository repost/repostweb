#! /usr/bin/env python

import feedparser
import optparse
import time
import calendar
import repost
import re

# sub reddits to get
reddits = ['pics']

# Old id hash table with time based clearing
class oldPosts(object):
    def __init__(self):
        self.ids = {};

    def addID(self, id):
        if( not self.ids.has_key(id) ):
                self.ids[id] = time.gmtime();
    
    def has_key(self, id):
        return self.ids.has_key(id)

    def removeOlderThan(self, seconds):
        gmt = calendar.timegm(time.gmtime()) - seconds
        for key, val in self.ids.items():
            if( val < gmt ):
                self.ids.pop(key)

def getLink(summary):
    #this will break very easily. Need to work on it
    linkstr = "<br /> <a href=\"(.*?)\">\[link]"
    return re.findall(linkstr,summary)
    

def controller():
    
    r = repost.Client()
    r.connect("test@j.sideramota.com","password")

    olds = oldPosts();
    
    # only get stuff which is top 100 and not sent before
    lasttime = 0
    while(1):
        # Let xmpppy do its thing
        r.process()
        now = time.time()
        if( (now - lasttime) > 120 ):
            lasttime = now
            feed = feedparser.parse("http://www.reddit.com/r/pics.rss");
            # check if they are new or old entries
            print "Entries " + str(len(feed.entries))
            for ent in feed.entries:
                if( not olds.has_key(ent.id) ):
                    # do something with new ones
                    image = getLink( ent.summary)
                    r.sendPicPost(ent.title, image, ent.id)
                    olds.addID(ent.id)
            # lets clear out the old ones so we don't overflow 
            olds.removeOlderThan(60*60)


def main():
    controller()

if __name__ == '__main__':
    main()
