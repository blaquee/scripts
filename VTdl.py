#!/usr/bin/python

import json
import datetime
import optparse
import urllib
import urllib2
import os
import ssl

#FUNCTIONS
def VTDownload(i):
	try:
		global vdir
		URL = "https://www.virustotal.com/intelligence/download/?hash=" + i + "&apikey=" + VTAPIKEY
		c = ssl._create_unverified_context()
		f = vdir + i
		print "Downloading " + URL + " to " + f
		urllib.urlretrieve(URL, f, context=c)
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	global VTAPIKEY
	global vdir

	parser = optparse.OptionParser('usage python VTdl.py <-f filename> ')
	
	parser.add_option('-f', '--filename', dest='filename', type='string', help='required specify filename of hashes to read')

	(options, args) = parser.parse_args()

	if (options.filename == None): 
		print parser.usage 
		exit (0)

	fn = options.filename
	
	vdir = os.getcwd() + os.sep + "VTdl" + os.sep
	if not os.path.exists(vdir):
		os.mkdir(vdir)

	if not os.path.exists("vt.conf"):
		vtfn = open("vt.conf", "w+")
		VTAPIKEY = str(raw_input('Enter VirusTotal API key: '))
		vtfn.write(VTAPIKEY)
		vtfn.close()
	
	vtfn = open("vt.conf")
	VTAPIKEY = vtfn.readline().rstrip("\n")
	vtfn.close()

	try:
		with open(fn) as vlf:
			for i in vlf:
				i = i.rstrip("\n")
				VTDownload(i)
	except Exception as e:
		print 'Exception:', e.message

if __name__ == '__main__':
	main()
