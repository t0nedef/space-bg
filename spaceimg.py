#!/usr/bin/python

from bs4 import BeautifulSoup
from socket import timeout
import urllib.request, re, string

##
# Return the contents of a url
def geturl(url):
	content = urllib.request.urlopen(url, timeout=15)
	data = content.read()
	content.close()
	return BeautifulSoup(data)

##
# Find today's astronomy image
def getbg():
	# parse the page for image information
	## get the page
	base = "http://apod.nasa.gov/apod/"
	try:
		tree = geturl(base)
	# if the main page doesn't work, try a mirror
	except timeout:
		base = "http://www.star.ucl.ac.uk/~apod/apod/"
		try:
			tree = geturl(base)
		except timeout:
			return ""
	item = []
	## title
	i = tree.find_all('center')[1].b.string.strip()
	item.append(i)
	## description
	i = tree.find_all('p')
	i[3].clear()
	item.append(i[2].get_text().strip().replace('\n','<br>').replace('\xa0',''))
	## url
	try:
		i = tree.img.parent['href']
	except AttributeError as e: #no image
		# maybe video
		item.append("")
		item.append(getvideo(tree))
		return item
	# image
	if (i.find('http://') > -1):
		item.append(i)
	else:
		# filter potential leading space
		item.append(base+i.strip())
	item.append("")
	return item

##
# Parse for video file
# do this by looking for an iframe
def getvideo(tree):
	i = tree.find_all('iframe')
	if(len(i) == 0):
		return ""
	url = i[0]['src']
	r = re.compile(r'\?.+')
	url = r.sub('', str(url))
	return url

#
