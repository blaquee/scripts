#!/usr/bin/python

logo = """
  _________        .__  __    __                       
  \_   ___ \_______|__|/  |__/  |_  ___________________
  /    \  \/\_  __ \  \   __\   __\/ __ \_  __ \___   /
  \     \____|  | \/  ||  |  |  | \  ___/|  | \//    / 
   \______  /|__|  |__||__|  |__|  \___  >__|  /_____ |
          \/                           \/            \/

 Input: text file with hash, ip, or domain on each line
 Output: JSON CRITS response, Fidelis Feed Format, and CRITS URLs
 Opens CRITS browser tabs unless -q is specified.  You must have a valid CRITS session logged into your browser.
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
def cDomain(i, src, buck):
	try:
		url = 'https://' + SERVER + '/api/v1/domains/'
		data = {
		'api_key': APIKEY,
		'username': USERNAME,
		'domain': i,
		'source': src,
		'bucket_list': buck,
		}
		r = requests.post(url, data=data, verify=False, timeout=10)
		time.sleep(vSleep)
		params = {
		'api_key': APIKEY,
		'username': USERNAME,
		'c-domain': i,
		}
		r = requests.get(url, params=params, verify=False, timeout=10)
		parsed = json.loads(r.content)
		print json.dumps(parsed, indent=4, sort_keys=True)
		vtgetResultsDomain(i)
	except Exception as e:
		print 'Exception:', e.message

def cIP(i, src, buck):
	try:
		url = 'https://' + SERVER + '/api/v1/ips/'
		data = {
		'api_key': APIKEY,
		'username': USERNAME,
		'ip': i,
		'ip_type': "Address - ipv4-addr",
		'source': src,
		'bucket_list': buck,
		}
		r = requests.post(url, data=data, verify=False, timeout=10)
		time.sleep(vSleep)
		params = {
		'api_key': APIKEY,
		'username': USERNAME,
		'c-ip': i,
		}
		r = requests.get(url, params=params, verify=False, timeout=10)
		parsed = json.loads(r.content)
		print json.dumps(parsed, indent=4, sort_keys=True)
		vtgetResultsIP(i)
	except Exception as e:
		print 'Exception:', e.message

def cmd5(i, src, buck):
	try:
		vtreScanMD5(i)
		time.sleep(2)
		i = vtgetResultsMD5(i)
		url = 'https://' + SERVER + '/api/v1/samples/'
		data = {
		'api_key': APIKEY,
		'username': USERNAME,
		'md5': i,
		'upload_type': "metadata",
		'source': src,
		'bucket_list': buck,
		}
		r = requests.post(url, data=data, verify=False, timeout=10)
		time.sleep(vSleep)
		params = {
		'api_key': APIKEY,
		'username': USERNAME,
		'c-md5': i,
		}
		r = requests.get(url, params=params, verify=False, timeout=10)
		parsed = json.loads(r.content)
		print json.dumps(parsed, indent=4, sort_keys=True)
	except Exception as e:
		print 'Exception:', e.message

def cCampaign(camp, desc, buck):
	try:
		url = 'https://' + SERVER + '/api/v1/campaigns/'
		data = {
		'api_key': APIKEY,
		'username': USERNAME,
		'name': camp,
		'description': desc,
		'bucket_list': buck,
		}
		r = requests.post(url, data=data, verify=False, timeout=10)
		time.sleep(vSleep)
		params = {
		'api_key': APIKEY,
		'username': USERNAME,
		'c-campaign.name': camp,
		}
		r = requests.get(url, params=params, verify=False, timeout=10)
		parsed = json.loads(r.content)
		print json.dumps(parsed, indent=4, sort_keys=True)
	except Exception as e:
		print 'Exception:', e.message

def cRelationship(ltype, lid, rtype, rid, reltype):
	try:
		url = 'https://' + SERVER + '/api/v1/relationships/'
		data = {
		'api_key': APIKEY,
		'username': USERNAME,
		'left_type': ltype,
		'left_id': lid,
		'right_type': rtype,
		'right_id': rid,
		'rel_type': reltype,
		}
		print str(data)
		r = requests.post(url, data=data, verify=False, timeout=10)
		time.sleep(vSleep)
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	parser = optparse.OptionParser('usage python critterz.py <-m mode> <-f filename> [-s intelSource] [-d feedDescription] [-b bucket] [ -q ] \n\n example: python critterz.py -m ip -f ip.txt -s TRT -d "Evil related" -b EvilMalware -c EvilCampaign')
	
	parser.add_option('-m', '--mode', dest='mode', type='string', help='required specify CRITs mode of either < domain | ip | md5 >')
	parser.add_option('-f', '--filename', dest='filename', type='string', help='required specify filename')
	parser.add_option('-s', '--source', dest='source', type='string', help='optional specify source of intel (Defaults to TRT)')
	parser.add_option('-d', '--description', dest='description', type='string', help='optional specify feed description (Defaults to bucket entry or Unknown if bucket is empty)')
	parser.add_option('-b', '--bucket', dest='bucket', type='string', help='optional specify CRITs bucket (Defaults to Unknown)')
	parser.add_option("-q", action="store_true", dest="quiet", help="optional quiet mode will not open browswer tabs")
	#parser.add_option('-c', '--campaign', dest='campaign', type='string', help='optional specify CRITs campaign (Defaults to Unknown)')

	(options, args) = parser.parse_args()

	if (options.mode == None) | (options.filename == None): 
		print parser.usage 
		exit (0)

	cm = options.mode
	fn = options.filename

	if (options.source == None):
		src = "TRT"
	else:
		src = options.source

	if (options.description == None):
		if (options.bucket != None):
			desc = options.bucket
		else:
			desc = "Unknown"
	else:
		desc = options.description

	if (options.bucket == None):
		buck = "Unknown"
	else: 
		buck = options.bucket

	if (options.quiet == True):
		quiet = "True"
	else:
		quiet = "False"

	requests.packages.urllib3.disable_warnings()
	fn = open(fn)
	dt = datetime.date.today().strftime('%m/%d/%Y')
	new = 2
	
	'''
	if (options.campaign == None):
		camp = "Unknown"
	else:	
		camp = options.campaign
	if camp != "Unknown":
		cCampaign(camp,desc,buck)
	'''

	global SERVER
	global USERNAME
	global APIKEY

	if not os.path.exists("crits.conf"):
		cfn = open("crits.conf", "w+")
		SERVER = str(raw_input('Enter Server: ')) + "\n"
		USERNAME = str(raw_input('Enter Username: ')) + "\n"
		APIKEY = str(raw_input('Enter API Key: ')) + "\n"
		cfn.write(SERVER)
		cfn.write(USERNAME)
		cfn.write(APIKEY)
		cfn.close()
	
	cfn = open("crits.conf")
	SERVER = cfn.readline().rstrip("\n")
	USERNAME = cfn.readline().rstrip("\n")
	APIKEY = cfn.readline().rstrip("\n")
	cfn.close()

	if cm == "domain":
		a = []
		for i in fn:
	   		i = i.rstrip("\n")
			cDomain(i,src,buck)
			a.append(i)
			time.sleep(vSleep)
		
		print "\n *** Feed Syntax *** \n"
		for c in range(len(a)):
			print 'url,' + a[c] + ',' + desc + ',' + dt + ',,'
		
		print "\n *** CRITs URLs *** \n"
		for b in range(len(a)):
			url = 'https://' + SERVER + '/domains/details/'+ a[b] + '/#analysis_button'
			print url
			if quiet == "False":
				webbrowser.open(url,new=new)
				time.sleep(vSleep)

	elif cm == "ip":
		a = []
		for i in fn:
	   		i = i.rstrip("\n")
			cIP(i,src,buck)
			a.append(i)
			time.sleep(vSleep)

		print "\n *** Feed Syntax *** \n"
		for c in range(len(a)):
			print 'ip,' + a[c] + ',' + desc + ',' + dt + ',,'

		print "\n *** CRITs URLs *** \n"
		for b in range(len(a)):
			url = 'https://' + SERVER + '/ips/details/'+ a[b] + '/#analysis_button'
			print url
			if quiet == "False":
				webbrowser.open(url,new=new)
				time.sleep(vSleep)

	elif cm == "md5":
		a = []
		ftype = str(raw_input('Enter filetype [pe]: '))
		malname = str(raw_input('Enter malware name [Trojan.Win.EvilName.fss1]: '))
		maltype = str(raw_input('Enter malware type [Trojan]: '))
		alast = str(raw_input('Enter analyst last name [ProtectorOfTheRealm]: '))
		
		for i in fn:
	   		i = i.rstrip("\n")
			cmd5(i,src,buck)
			a.append(i)
			time.sleep(vSleep)
		
		print "\n *** Feed Syntax *** \n"
		for c in range(len(a)):
			print a[c] + ',,' + ftype + ',' + malname + ',' + maltype + ',4,' + desc + ',' + alast

		print "\n *** CRITs URLs *** \n"
		for b in range(len(a)):
			url = 'https://' + SERVER + '/samples/details/'+ a[b] + '/#analysis_button'
			print url
			if quiet == "False":
				webbrowser.open(url,new=new)
				time.sleep(vSleep)
	else:
		print parser.usage 

if __name__ == '__main__':
	main()
