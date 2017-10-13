#!/usr/bin/env python
# SmbShakedown 2.0
# Script: smptconnect.py
# Description: SMTP client
# Author(s): Nick Sanzotta
# Version: v 2.12132017

try:
    import sys
    import smtplib
    import readline
    readline.parse_and_bind("tab: complete")
except Exception as e:
    print('[!] SMTPCONNECT - Error: %s' % (e))
    sys.exit(1)


class SmtpConnect():
    def __init__(self, provider, port, user,
                 passwd, sender, recipient, message):
        self.provider = provider
        self.user = user
        self.passwd = passwd
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.port = port

        # Connect to smtp provider
        try:
            smtpserver = smtplib.SMTP(self.provider, self.port)
            self.status = smtpserver.noop()
            # Connection Response
            print('Connection response: %s' % (self.status[0]))
        except Exception as e:
            errno, message = e.args
            if errno == -2:
                print('[!] Error: SMTP Server name not known')
            else:
                print('[!] Error: %s %s' % (errno, message))
            sys.exit(1)

        # Send ehlo
        smtpserver.ehlo()
        print('EHLO response: %s' % (self.status[0]))

        # Start TLS
        try:
            smtpserver.starttls()
            print('TLS response: %s' % (self.status[0]))
        except Exception as e:
            errno, message = e.args
            print('[!] Error: %s %s' % (errno, message))

        # Login
        try:
            smtpserver.login(self.user, self.passwd)
            print('Login response: %s' % (self.status[0]))
        except (Exception) as e:
            errno, message = e.args
            if errno == 535:
                print('[!] Error: Login Failure.')
            elif errno == 534:
                print("[!] Error: 'Allow less secure apps' is set to: OFF.")
            else:
                print('[!] Error: %s %s' % (errno, message))
            sys.exit(1)

        # Print email message
        print('\n')
        print('MAIL FROM: %s' % (self.sender))
        print('RCPT TO: %s' % (self.recipient))
        print('\n')
        print('Batch Message Preview:\n%s' % (self.message))
        print('\n')

        # Send Mail
        try:
            smtpserver.sendmail(self.sender, self.recipient, self.message)
            print('Send mail response: %s' % (self.status[0]))
            smtpserver.quit()
        except Exception as e:
            print(e)


# def sigint_handler(signum, frame):
#     print('(CTRL+C) Stopping...')
#     sys.exit(0)

# signal.signal(signal.SIGINT, sigint_handler)

# if __name__ == "__main__":

#     smtpConnect = SmtpConnect()
