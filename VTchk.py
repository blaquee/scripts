#!/usr/bin/python

logo = """
____   ________________________ .__     __    
\   \ /   /\__    ___/\_   ___ \|  |__ |  | __
 \   Y   /   |    |   /    \  \/|  |  \|  |/ /
  \     /    |    |   \     \___|   Y  \    < 
   \___/     |____|    \______  /___|  /__|__|
 Input: text file with hash, ip, domain, or URL on each line
 Output: JSON VirusTotal results
"""

print logo

import json
import datetime
import optparse
import webbrowser
import time
import urllib
import urllib2
import os
import ssl

try:
	import simplejson
except ImportError:
	print "Couldnt import simplejson. \n Try: 'sudo pip install simplejson'"
try:
	import requests
except ImportError:
	print "Couldnt import requests. \n Try: 'sudo pip install requests and sudo pip install requests[security]'"

dict = {}
vSleep = 1

#FUNCTIONS
def vtreScanMD5(i):
	try:
		url = "https://www.virustotal.com/vtapi/v2/file/rescan"
		parameters = {"resource": i, "apikey": VTAPIKEY}
		data = urllib.urlencode(parameters)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		json_object = response.read()
		response_dict = json.loads(json_object)
		vtresponse = int(response_dict.get("response_code",{}))
		if vtresponse == 1:
			print "Queued Rescan for: " + i
		else:
			print "Error Trying Rescan for: " + i + " (Might be missing)"
	except Exception as e:
		print 'Exception:', e.message

def vtMD5(i):
	try:
		url = "https://www.virustotal.com/vtapi/v2/file/report"
		parameters = {"resource": i, "apikey": VTAPIKEY}
		data = urllib.urlencode(parameters)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		json_object = response.read()
		response_dict = json.loads(json_object)
		print json.dumps(response_dict, indent=4, sort_keys=True)
		vtmd5 = str(response_dict.get("md5",{}))
		kdetect = str(response_dict.get("scans",{}).get("Kaspersky").get("detected",{}))
		kname = str(response_dict.get("scans",{}).get("Kaspersky").get("result",{}))
		if vtmd5 == "{}":
			dict[i] = kdetect + ", " + kname
		else:
			dict[vtmd5] = kdetect + ", " + kname
	except Exception as e:
		print 'Exception:', e.message

def vtIP(i):
	try:
		url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
		parameters = {'ip': i, 'apikey': VTAPIKEY}
		response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
		response_dict = json.loads(response)
		print json.dumps(response_dict, indent=4, sort_keys=True)
	except Exception as e:
		print 'Exception:', e.message

def vtDomain(i):
	try:
		url = 'https://www.virustotal.com/vtapi/v2/domain/report'
		parameters = {'domain': i, 'apikey': VTAPIKEY}
		response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
		response_dict = json.loads(response)
		print json.dumps(response_dict, indent=4, sort_keys=True)
	except Exception as e:
		print 'Exception:', e.message

def vtURL(i):
	try:
		url = "https://www.virustotal.com/vtapi/v2/url/report"
		parameters = {"resource": i, "apikey": VTAPIKEY}
		data = urllib.urlencode(parameters)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		json_object = response.read()
		if "\"result\": \"phishing site\"" in json_object or "\"result\": \"malicious site\"" in json_object:
			dict[i] = "EVIL"
		else:
			dict[i] = "CLEAN"
		json_print = json.loads(json_object)
		print json.dumps(json_print, indent=4, sort_keys=True)
	except Exception as e:
		print 'Exception:', e.message

def VTCluster(i):
	try:
		params = {'apikey': VTAPIKEY, 'resource': i}
		response = requests.get('https://www.virustotal.com/vtapi/v2/file/clusters', params=params)
		response_json = response.json()
		print response_json
	except Exception as e:
		print 'Exception:', e.message

def VTBehav(i):
	try:
		params = {'apikey': VTAPIKEY, 'resource': i}
		response = requests.get('https://www.virustotal.com/vtapi/v2/file/behaviour', params=params)
		response_json = response.json()
		print response_json
	except Exception as e:
		print 'Exception:', e.message

def VTNet(i):
	try:
		params = {'apikey': VTAPIKEY, 'resource': i}
		response = requests.get('https://www.virustotal.com/vtapi/v2/file/network-traffic', params=params)
		response_json = response.json()
		print response_json
	except Exception as e:
		print 'Exception:', e.message

def VTDownload(i):
	try:
		URL = "https://www.virustotal.com/intelligence/download/?hash=" + i + "&apikey=" + VTAPIKEY
		c = ssl._create_unverified_context()
		f = vdir + i
		print "Downloading to " + f
		urllib.urlretrieve(URL, f, context=c)
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	global VTAPIKEY
	global vdir

	parser = optparse.OptionParser('usage python VTChk.py <-m mode> <-f filename> [-d directory]')
	
	parser.add_option('-m', '--mode', dest='mode', type='string', help='mode < domain | ip | hash | url >')
	parser.add_option('-f', '--filename', dest='filename', type='string', help='required specify filename')
	parser.add_option('-d', '--dir', dest='directory', type='string', help='optional specify directory if you want to download files')

	(options, args) = parser.parse_args()

	if (options.mode == None) | (options.filename == None): 
		print parser.usage 
		exit (0)

	cm = options.mode
	fn = options.filename
	vdir = options.directory

	if not os.path.exists("vt.conf"):
		vtfn = open("vt.conf", "w+")
		VTAPIKEY = str(raw_input('Enter VirusTotal API key: '))
		vtfn.write(VTAPIKEY)
		vtfn.close()
	
	vtfn = open("vt.conf")
	VTAPIKEY = vtfn.readline().rstrip("\n")
	vtfn.close()

	if vdir == None:
		vdl = 0
	else:
		if not os.path.exists(vdir):
			os.mkdir(vdir)
		vdl = 1

	requests.packages.urllib3.disable_warnings()
	fn = open(fn)

	if cm == "domain":
		for i in fn:
	   		i = i.rstrip("\n")
			vtDomain(i)
			time.sleep(vSleep)

	elif cm == "url":
		for i in fn:
	   		i = i.rstrip("\n")
			vtURL(i)
			time.sleep(vSleep)

		print "\n *** EVIL / CLEAN *** \n"
		for key in dict:
			print key + ", " + dict[key]

	elif cm == "ip":
		for i in fn:
	   		i = i.rstrip("\n")
			vtIP(i)
			time.sleep(vSleep)

	elif cm == "hash":
		for i in fn:
	   		i = i.rstrip("\n")
	   		vtreScanMD5(i)
			time.sleep(vSleep)
			vtMD5(i)
			time.sleep(vSleep)
			VTCluster(i)
			time.sleep(vSleep)
			VTBehav(i)
			time.sleep(vSleep)
			VTNet(i)
			time.sleep(vSleep)
			if vdl == 1:
				VTDownload(i)
				time.sleep(vSleep)

		print "\n *** KASPERSKY Results*** \n"
		for key in dict:
			print key + ", " + dict[key]

	else:
		print parser.usage 

if __name__ == '__main__':
	main()