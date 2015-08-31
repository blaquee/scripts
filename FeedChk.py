#!/usr/bin/python

import optparse
import os

def UpdateGit():
	try:
		print "[+] Attempting git pull to get the latest"
		os.system("git -C " + GITDIR + " pull")
	except Exception as e:
		print 'Exception:', e.message

def CheckGit(i):
	try:
		if i in feedfile.read():
			print "*** " + i + " Found in Feed Already ***"
		else:
			print i + " Not Found in Feed"
		feedfile.seek(0)
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():
	parser = optparse.OptionParser('usage python FeedChk.py <-m mode> <-f filename> [-p specify to pull from git first]')
	
	parser.add_option('-m', '--mode', dest='mode', type='string', help='required specify mode < domain | hash >')
	parser.add_option('-f', '--filename', dest='filename', type='string', help='required specify filename')
	parser.add_option("-p", action="store_true", dest="pull", help="optional specify to perform a git pull to check the latest")
	
	(options, args) = parser.parse_args()

	if (options.mode == None) | (options.filename == None): 
		print parser.usage 
		exit (0)

	cm = options.mode
	fn = options.filename
	
	fn = open(fn)
	
	if not os.path.exists("feedchk.conf"):
		ffn = open("feedchk.conf", "w+")
		GITDIR = str(raw_input('Enter GIT Directory: ')) + "\n"
		ffn.write(GITDIR)
		ffn.close()
	
	ffn = open("feedchk.conf")
	GITDIR = ffn.readline().rstrip("\n")
	
	if (options.pull == True):
		UpdateGit()
	else:
		print "[+] -p not specified not updating Git"
	
	global feedfile
	if cm == "domain":
		feedfile = open(GITDIR + "build_scripts/feed/intel.csv")
		for i in fn:
	   		i = i.rstrip("\n")
			CheckGit(i)
	elif cm == "hash":
		feedfile = open(GITDIR + "build_scripts/feed/md5.csv")
		for i in fn:
	   		i = i.rstrip("\n")
			CheckGit(i)
	else:
		print parser.usage 

if __name__ == '__main__':
	main()
