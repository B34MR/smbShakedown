# Script: arguments.py
# Description: smbShakedown arguments
# Author(s): Nick Sanzotta
# Version: v 2.12132017

import argparse

# Removed default usage prefix
class HelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = ''
        return super(HelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

# Create Parser
def parse_args():
    parser = argparse.ArgumentParser(formatter_class=HelpFormatter)

    smtp_group = parser.add_argument_group('SMTP Client')
    smtp_group.add_argument('--relay', type=str.lower, metavar='', default='', help='SMTP Relay Server' )
    smtp_group.add_argument('--port', type=int, metavar='', help='SMTP Port')
    smtp_group.add_argument('--user', type=str.lower, metavar='', default='', help='SMTP User Account')
    smtp_group.add_argument('--pass', dest='passwd', type=str, metavar='', default='', help='SMTP Account Password')
    smtp_group.add_argument('--mail_from', type=str.lower, metavar='', default='', help='MAIL FROM:')
    smtp_group.add_argument('--rcpt', type=str, metavar='', default='', help='RCPT TO:')
    smtp_group.add_argument('--template', type=int, metavar='', default='1', help='Define email message template')
    smtp_group.add_argument('--templates', action='store_true', default=False, help='List available email message templates')
    smtp_group.add_argument('--from_header', type=str, metavar='', default='', help='"From" Header')
    smtp_group.add_argument('--rcpt_header', type=str, metavar='', default='', help='"To" Header')
    smtp_group.add_argument('--limit', type=int, metavar='', default=20, help='Maximum number of BCC email addresses to send at once')
    smtp_group.add_argument('--delay', type=int, metavar='', default=0, help='Delay between emails sent (in minutes)')

    smb_group = parser.add_argument_group('SMB Server (Not available, currently in development)')
    smb_group.add_argument('--smb_ip', type=str.lower, metavar='', default='0.0.0.0', help='SMB server address')
    smb_group.add_argument('--smb', action='store_true', help='Initialize SMB Server')
    smb_group.add_argument('--share_name', type=str.lower, metavar='', default='smbShakedown', help='')
    smb_group.add_argument('--share_path', type=str.lower, metavar='', default='/tmp/', help='')
    smb_group.add_argument('--share_comment', type=str.lower, metavar='', default='smbShakedown Server', help='')
    smb_group.add_argument('--server_port', type=int, metavar='', default=445, help='')
    smb_group.add_argument('--smbchallenge', type=str, metavar='[Default] Random', default='', help='')
    smb_group.add_argument('--smb2support', type=bool, metavar='', default=False, help='')
    smb_group.add_argument('--log_file', type=str, metavar='', default='', help='')
    smb_group.add_argument('--debug', action='store_true', default=False, help='')

    http_group = parser.add_argument_group('HTTP Server (Not available, currently in development)')
    http_group.add_argument('--http', action='store_true', help='Launch HTTP Server')

    # Create parser instance
    args = parser.parse_args()

    # Checks for arguments that require --port option.
    if args.relay and not args.port:
        parser.error(args.relay + ' requires --port')
    elif args.relay and not args.sender:
        parser.error(args.relay + ' requires --sender')

    # Return arg values
    return args
