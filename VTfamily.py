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
def VTSearch(vfamily, vengine, vtype, vdate):
	try:
		params = {'apikey': VTAPIKEY, 'query': vengine + ':' + vfamily + ' type:' + vtype + ' fs:' + vdate}
		response = requests.get('https://www.virustotal.com/vtapi/v2/file/search', params=params)
		response_json = response.json()
		time.sleep(2)
		for i in response_json.get("hashes",{}):
			print i
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	global VTAPIKEY

	parser = optparse.OptionParser('usage python VTdata.py -f <family> [-e engines] [-t peexe] [-d 1] \n\n Default engines searches all AV engines for family name \n\n options: a_squared ad_aware aegislab agnitum ahnlab ahnlab_v3 alibaba alyac antivir antivir7 antiy_avl arcabit authentium avast avg avira avware baidu bitdefender bkav bytehero cat_quickheal clamav cmc commtouch comodo cyren drweb emsisoft esafe escan eset_nod32 f_prot f_secure fortinet gdata ikarus jiangmin k7antivirus k7gw kaspersky kingsoft malwarebytes mcafee mcafee_gw_edition microsoft microworld_escan nano_antivirus nod32 norman nprotect panda pctools prevx prevx1 qihoo_360 rising sophos sunbelt superantispyware symantec tencent thehacker totaldefense trendmicro trendmicro_housecall vba32 vipre virobot zillya zoner')
	
	parser.add_option('-f', '--family', dest='vfamily', type='string', help='required specify malware family')
	parser.add_option('-e', '--engine', dest='vengine', type='string', help='optional specify AV Engine Default: [engines]')
	parser.add_option('-t', '--type', dest='vtype', type='string', help='optional specify type Default: [peexe]')
	parser.add_option('-d', '--days', dest='vdate', type='string', help='optional days after first submission Default: [1]')

	(options, args) = parser.parse_args()

	if (options.vfamily == None): 
		print parser.usage 
		exit (0)
	else:
		vfamily = options.vfamily

	if (options.vengine == None):
		vengine = "engines"
	else:
		vengine = options.vengine
	
	if (options.vtype == None):
		vtype = "peexe"
	else:
		vtype = options.vtype

	if (options.vdate == None):
		vdate = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00') + "+"
	else:
		vdate = (datetime.date.today() - datetime.timedelta(days=options.vdate)).strftime('%Y%m%dT00:00:00') + "+"

	if not os.path.exists("vt.conf"):
		vtfn = open("vt.conf", "w+")
		VTAPIKEY = str(raw_input('Enter VirusTotal API key: '))
		vtfn.write(VTAPIKEY)
		vtfn.close()
	
	vtfn = open("vt.conf")
	VTAPIKEY = vtfn.readline().rstrip("\n")
	vtfn.close()

	VTSearch(vfamily, vengine, vtype, vdate)

if __name__ == '__main__':
	main()
