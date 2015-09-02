#!/usr/bin/python

logo = """
________    _________.___ ____________________________
\_____  \  /   _____/|   |\      \__    ___/\____    /
 /   |   \ \_____  \ |   |/   |   \|    |     /     / 
/    |    \/        \|   /    |    \    |    /     /_ 
\_______  /_______  /|___\____|__  /____|   /_______ |


Downloads various open source lists to current_dir/oDL/*
"""

'''
http://antispam.imp.ch/spamlist
http://aptnotes.malwareconfig.com/ioc_export.csv
http://atrack.h3x.eu/
http://autoshun.org/files/shunlist.csv
http://blocklist.greensnow.co/greensnow.txt
http://cinsscore.com/list/ci-badguys.txt
http://cybercrime-tracker.net/all.php
http://danger.rulez.sk/projects/bruteforceblocker/blist.php
http://data.phishtank.com/data/online-valid.csv
http://doc.emergingthreats.net/pub/Main/RussianBusinessNetwork/RussianBusinessNetworkIPs.txt
http://dragonresearchgroup.org/insight/http-report.txt
http://dragonresearchgroup.org/insight/sshpwauth.txt
http://dragonresearchgroup.org/insight/vncprobe.txt
http://hosts-file.net/rss.asp
http://labs.snort.org/feeds/ip-filter.blf
http://lists.blocklist.de/lists/all.txt
http://malc0de.com/bl/IP_Blacklist.txt
http://malc0de.com/rss/
http://malwaredb.malekal.com/export.php?type=url
http://mirror1.malwaredomains.com/files/domains.txt
http://nullsecure.org/threatfeed/master.txt
http://osint.bambenekconsulting.com/feeds/c2-masterlist.txt
http://osint.bambenekconsulting.com/feeds/dga-feed.txt
http://reputation.alienvault.com/reputation.data
http://rules.emergingthreats.net/blockrules/compromised-ips.txt
http://sysctl.org/cameleon/hosts
http://vxvault.net/URL_List.php
http://www.blocklist.de/lists/bruteforcelogin.txt
http://www.chaosreigns.com/iprep/iprep.txt
http://www.dshield.org/ipsascii.html?limit=10000
http://www.malwaredomainlist.com/mdlcsv.php
http://www.nothink.org/blacklist/blacklist_malware_http.txt
http://www.nothink.org/blacklist/blacklist_ssh_all.txt
http://www.openbl.org/lists/base.txt
http://www.spamhaus.org/drop/drop.txt
http://www.us.openbl.org/lists/base.txt
https://check.torproject.org/exit-addresses
https://dshield.org/block.txt
https://dshield.org/feeds/suspiciousdomains_High.txt
https://dshield.org/feeds/suspiciousdomains_Low.txt
https://dshield.org/feeds/suspiciousdomains_Medium.txt
https://palevotracker.abuse.ch/?rssfeed
https://spam404bl.com/spam404scamlist.txt
https://sslbl.abuse.ch/blacklist/dyre_sslblacklist.csv
https://sslbl.abuse.ch/blacklist/dyre_sslipblacklist.csv
https://sslbl.abuse.ch/blacklist/sslblacklist.csv
https://sslbl.abuse.ch/blacklist/sslipblacklist.csv
https://virbl.bit.nl/download/virbl.dnsbl.bit.nl.txt
https://www.badips.com/get/list/http/0
https://www.badips.com/get/list/mail/0
https://www.badips.com/get/list/ssh/0
https://www.binarydefense.com/banlist.txt
https://www.openphish.com/feed.txt
https://www.packetmail.net/iprep.txt
https://zeustracker.abuse.ch/rss.php
#####
Not added
http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-1.uceprotect.net.gz
http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-2.uceprotect.net.gz
http://wget-mirrors.uceprotect.net/rbldnsd-all/dnsbl-3.uceprotect.net.gz
https://www.c1fapp.com/cifapp/lists/
'''

print logo

import urllib
import os
import ssl
import itertools
import re

def oSetup():
	try:
		global dir
		if not os.path.exists(dir):
			os.mkdir(dir)
			print "[+] Creating " + str(dir)
		else:
			print "[*] Already Exists " + str(dir)
	except Exception as e:
		print 'Exception:', e.message

def oTry():
	try:
		global dir
		c = 1
		with open(os.getcwd() + "/osintz.py") as fn:
			for i in itertools.islice(fn, 14, 69):
				i = i.rstrip("\n")
				f = dir + str(c)
				print "[+] " + str(c) + "/55 Downloading: " + i + " to: " + f
				oDL(i, f)
				c = c + 1
	except Exception as e:
		print 'Exception:', e.message

def oDL(i, f):
	try:
		if i[4] == "s":
			ctxt = ssl._create_unverified_context()
			urllib.urlretrieve(i, f, context=ctxt)
		else: 
			urllib.urlretrieve(i, f)
	except Exception as e:
		print 'Exception:', e.message

def oIP():
	try:
		global dir
		print "[+] Creating master IP list: " + dir + "IP_Master.txt"
		ipd = []
		r = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
		fl = os.listdir(dir)
		for fln in fl: 
			with open(dir + fln) as fn:
				for i in fn:
					chk = r.findall(i)
					for c in chk:
						if c is not None: #and c not in ipd:
							ipd.append(c)
		
		try:
			fw = open(dir + "IP_Master.txt", "w")
			for ip in set(ipd):
				fw.write(ip + "\n")
		except Exception as e:
			print 'Exception:', e.message

	except Exception as e:
		print 'Exception:', e.message


def main():
	global dir
	dir = os.getcwd() + "/oDL/"
	#oSetup()
	#oTry()
	oIP()

if __name__ == '__main__':
	main()