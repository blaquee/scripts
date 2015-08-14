#!/usr/bin/python

import os
import optparse

#FUNCTIONS
def PCAPparse(pcap):
	try:
		print os.system("tshark -r " + pcap + " -z hosts | grep -A 999999999999999 \"# TShark hosts output\"")
		print os.system("tshark -r " + pcap + " -z http_req,tree | grep -A 999999999999999 \"==============================\"")
	except Exception as e:
		print 'Exception:', e.message

#MAIN
def main():

	parser = optparse.OptionParser('usage python PCAPstats.py [-p PCAPfile]')
	
	parser.add_option('-p', '--pcap', dest='pcap', type='string', help='optional specify pcap file otherwise parses all PCAPS in current directory')

	(options, args) = parser.parse_args()

	if (options.pcap == None):
		os.system("mergecap -a -w PCAPSTATSmerged.pcap *.pcap")
		pcap = "PCAPSTATSmerged.pcap" 
	else:
		pcap = options.pcap

	PCAPparse(pcap)

	if (pcap == "PCAPSTATSmerged.pcap"):
		os.system("rm -f PCAPSTATSmerged.pcap")

if __name__ == '__main__':
	main()
