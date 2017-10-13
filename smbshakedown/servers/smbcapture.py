#!/usr/bin/env python
# SmbShakedown 2.0
# Script: smbcapture.py
# Description: SMB capture server
# Author(s): Nick Sanzotta
# Version: v 2.12132017
try:
    import os
    import sys
    import signal
    import random
    # import logging
    from impacket import smbserver
except Exception as e:
    print('[!] SMBSERVER - Module Import Error: %s' % (e))
    sys.exit(1)


class SmbCapture():
    def __init__(self, share_name, share_path, share_comment, smb_ip,
                 server_port, smbchallenge, smb2support, log_file, debug):
        self.share_name = share_name.upper()
        self.share_path = os.path.realpath(share_path)
        self.share_comment = share_comment
        self.smb_ip = smb_ip
        self.server_port = server_port
        # Must be 16 hex bytes long defaults to '4141414141414141'
        self.smbchallenge = smbchallenge
        self.smb2support = smb2support
        self.debug = debug
        self.log_file = log_file

        # Set IP and port
        try:
            self.smb_server =\
                smbserver.SimpleSMBServer(self.smb_ip, self.server_port)
        except Exception as e:
            errno, message = e.args
            if errno == 98 and message == 'Address already in use':
                print('[!] SMBSERVER - Error: Port %s is already in use' % (self.server_port))
            else:
                print('[!] SMBSERVER - Error: %s' % (e))
            sys.exit(1)

        # Set share name, path and comment
        self.smb_server.addShare(self.share_name, self.share_path, self.share_comment)

        # Set challenge to random hex value if not defined
        if self.smbchallenge == '':
            random = self.random_challenge()
            self.smb_server.setSMBChallenge(random)
        else:
            self.smb_server.setSMBChallenge(self.smbchallenge)

        # Set SMBv2 support on/off
        self.smb_server.setSMB2Support(self.smb2support)

        # Set Logger
        self.smb_server.setLogFile(self.log_file)

        # Launch SMB server
        print(' [*] Starting the SMB Server')
        print(' [*] SMB Server IP: %s' % (self.smb_ip))
        print(' [*] SMB Server Port: %s' % (self.server_port))
        print(' [*] SMB Challenge set: %s' % (random))
        self.smb_server.start()

    def random_challenge(self):
        challenge =\
            ''.join(random.choice('0123456789abcdef') for n in xrange(16))
        return challenge


def sigint_handler(signum, frame):
    print('(CTRL+C) Stopping...')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# if __name__ == "__main__":
#     smbServer = SmbCapture('smbShakedown', '/tmp/', 'Test', '0.0.0.0', 445, '', False, '', False)
