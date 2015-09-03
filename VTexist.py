#!/usr/bin/python

logo = """
____   _______________           .__          __   
\   \ /   /\__    ___/___ ___  __|__| _______/  |_ 
 \   Y   /   |    |_/ __ ||  \/  /  |/  ___/\   __|
  \     /    |    |\  ___/ >    <|  |\___ \  |  |  
   \___/     |____| \___  >__/\_ \__/____  > |__|
 Input: CSV hashes
 Output: Hashes that exist in VT and downloads them
"""

print logo

import json
import datetime
import optparse
import urllib
import urllib2
import os
import ssl
import csv
from time import gmtime, strftime

#FUNCTIONS

def vtMD5(i):
	try:
		url = "https://www.virustotal.com/vtapi/v2/file/report"
		parameters = {"resource": i, "apikey": VTAPIKEY, "allinfo": "1"}
		data = urllib.urlencode(parameters)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		json_object = response.read()
		response_dict = json.loads(json_object)
		#print json.dumps(response_dict, indent=4, sort_keys=True)
		vtmd5 = str(response_dict.get("md5",{}))
		vttype = str(response_dict.get("type",{}))
		if vtmd5 == "{}":
			return 0
		else:
			if ("EXE" in vttype.upper() or "DLL" in vttype.upper() or "MSI" in vttype.upper() or "PDF" in vttype.upper() or "DOC" in vttype.upper() or "PPT" in vttype.upper() or "XLS" in vttype.upper() or "FLA" in vttype.upper() or "HTM" in vttype.upper()  or "ZIP" in vttype.upper()): 
				return 1

	except Exception as e:
		print 'Exception:', e.message

def VTDownload(i):
	try:
		URL = "https://www.virustotal.com/intelligence/download/?hash=" + i + "&apikey=" + VTAPIKEY
		c = ssl._create_unverified_context()
		f = vdir + i
		print "Downloading " + f
		urllib.urlretrieve(URL, f, context=c)
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	global VTAPIKEY
	global vdir

	parser = optparse.OptionParser('usage python VTexist.py <-f filename> [-d directory]')
	
	parser.add_option('-f', '--filename', dest='filename', type='string', help='required specify csv with hashes')
	parser.add_option("-d", action="store_true", dest="dl", help="optional download mode will download found files")

	(options, args) = parser.parse_args()

	if (options.filename == None): 
		print parser.usage 
		exit (0)

	fn = options.filename
	dl = options.dl

	if not os.path.exists("vt.conf"):
		vtfn = open("vt.conf", "w+")
		VTAPIKEY = str(raw_input('Enter VirusTotal API key: '))
		vtfn.write(VTAPIKEY)
		vtfn.close()
	
	vtfn = open("vt.conf")
	VTAPIKEY = vtfn.readline().rstrip("\n")
	vtfn.close()

	if dl is None:
		vdl = 0
		print "-d not specified not downloading found samples\n"
	else:
		vdir = os.getcwd() + os.sep + "HashesVTexist" + os.sep
		if not os.path.exists(vdir):
			os.mkdir(vdir)
		vdl = 1
		print "-d was specified downloading found samples to " + vdir + "\n"
	
	resfile = "HashesVTexist_" + strftime("%Y%m%d_%H_%M_%S", gmtime()) + ".txt"
	results = open(resfile, "w")

	try:
		with open(fn) as csvf:
			hr = csv.reader(csvf, delimiter=",", quotechar='"')
			next(hr)
			c = 0
			found = 0
			for i in hr:
	   			c = c + 1
				ihash = i[1]
				e = vtMD5(ihash)
				if e == 1:
					found = found + 1
					print str(c) + " " + ihash + " TRUE " + " FOUND=" + str(found) 
					results.write(ihash + "\n")
					if vdl == 1:
						VTDownload(ihash)
				else:
					print str(c) + " " + ihash + " FALSE" + " FOUND=" + str(found) 
					
	except Exception as e:
		print 'Exception:', e.message

if __name__ == '__main__':
	main()
