#!/usr/bin/python

import json
import datetime
import optparse
import time
import os

try:
	import requests
except ImportError:
	print "Couldnt import requests. \n Try: 'sudo pip install requests and sudo pip install requests[security]'"

#FUNCTIONS
def VTSearch(vtag, vtype, vdate):
	try:
		params = {'apikey': VTAPIKEY, 'query': 'tag:' + vtag + ' type:' + vtype + ' fs:' + vdate}
		response = requests.get('https://www.virustotal.com/vtapi/v2/file/search', params=params)
		response_json = response.json()
		for i in response_json.get("hashes",{}):
			print i
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	global VTAPIKEY

	parser = optparse.OptionParser('usage python VTtag.py -g tag [-t peexe] [-d 1]')	
	parser.add_option('-g', '--tag', dest='vtag', type='string', help='specify tag https://www.virustotal.com/intelligence/help/')
	parser.add_option('-t', '--type', dest='vtype', type='string', help='specify type Default: [peexe]')
	parser.add_option('-d', '--days', dest='vdate', type='int', help='optional days after first submission Default: [1]')

	(options, args) = parser.parse_args()

	if (options.vtag == None):
		print parser.usage 
		exit (0)
	else:
		vtag = options.vtag
	
	if (options.vtype == None):
		vtype = "peexe"
	else:
		vtype = options.vtype

	if (options.vdate == None):
		vdate = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00') + "+"
	else:
		vdate = (datetime.date.today() - datetime.timedelta(days=options.vdate)).strftime('%Y-%m-%dT00:00:00') + "+"

	if not os.path.exists("vt.conf"):
		vtfn = open("vt.conf", "w+")
		VTAPIKEY = str(raw_input('Enter VirusTotal API key: '))
		vtfn.write(VTAPIKEY)
		vtfn.close()
	
	vtfn = open("vt.conf")
	VTAPIKEY = vtfn.readline().rstrip("\n")
	vtfn.close()
	print "[+] Searching for tag: " + vtag + " type: " + vtype + " date: " + vdate
	VTSearch(vtag, vtype, vdate)

if __name__ == '__main__':
	main()
