#! /usr/bin/env python

import feedparser
import optparse
import time
import calendar

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

def controller():
	
	olds = oldPosts();
	
	# only get stuff which is top 100 and not sent before
	x = 0
	y = 0
	while(1):

		feed = feedparser.parse("http://www.reddit.com/r/pics.rss");
		# check if they are new or old entries
		for ent in feed.entries:
			if( not olds.has_key(ent.id) ):
				# do something with new ones
				olds.addID(ent.id)
			x += 1
			if( x > 2):
				break

		y += 1
		# lets clear out the old ones so we don't overflow 
		if( (y % 5) == 0 ):
			y = 0
			olds.removeOlderThan(60*60)
		time.sleep(100)


def main():
	controller()

if __name__ == '__main__':
	main()
