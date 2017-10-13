# Script: core.py
# Description: Core script for smbShakedown
# Author(s): Nick Sanzotta
# Version: v 2.12132017
try:
    import readline
    readline.parse_and_bind("tab: complete")
    import os
    import sys
    import signal
    from subprocess import Popen, PIPE
    import time
    import csv
    import arguments
    from clients import smtpconnect
except Exception as e:
    print('[!] CORE - Error: %s' % (e))
    sys.exit(1)


def sigint_handler(signum, frame):
    print('(CTRL+C) Terminated')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def main():
    # Argparse arguments
    args = arguments.parse_args()

    # Recipient List
    recipient_list = []

    # Name List
    first_name_list = []
    last_name_list = []

    # Batch List.
    batch_list = []

    # Convert delay seconds to minutes
    delay = args.delay * 60

    # Build email template dictionary.
    template_dic = {}
    template_dir = 'templates/email/'
    template_number = 0
    templates = os.listdir(template_dir)
    for template in templates:
        if not template in 'active_template.txt':
            template_number += 1
            template_dic[template_number] = template

    # Create email function
    def create_email(recipients):
        try:
            template_choice = args.template
            selected_template = template_dic[template_choice]
        except ValueError as e:
            message = e.args
            print("[!] Error: Not an integer: %s" % (message))
            sys.exit(1)
        except KeyError as e:
            message = e.args
            print("[!] Error: Invalid selection: %s" % (message))
            sys.exit(1)

        # Create a List of template lines.
        template_path = template_dir + selected_template
        with open(template_path, 'r') as f:
            line = f.readlines()

        # Lines to modify in template.
        line[0] = 'From: %s <%s>\n' % (args.from_header, args.user)
        line[1] = 'To: %s <%s>\n' % (args.rcpt_header, recipients)
        line[2] = 'MIME-Version: 1.0\n'
        line[3] = 'Content-type: text/html\n'
        # line[6] =  'Hi %s, \n' % (first_name_list[0])
        line[-1] = '<img src=file://%s/sig.jpg height="100" width="150"></a>' % (args.smb_ip)

        with open('templates/email/active_template.txt', 'w') as f:
            f.writelines(line)

    # Parse recipient list.
    if args.rcpt:
        try:
            if 'csv' in args.rcpt:
                with open(args.rcpt, 'r') as f:
                    reader = csv.reader(f)
                    # Removes header, first row.
                    next(reader, None)
                    for recipient in reader:
                        recipient_list.append(recipient[0])
                        first_name_list.append(recipient[1])
                        last_name_list.append(recipient[2])
                    # print('\n')
                    # print('Recipient list:')
                    # print(recipient_list)

            elif 'txt' in args.rcpt:
                with open(args.rcpt, 'r') as f:
                    recipient = f.readlines()
                    for x in recipient:
                        recipient_list.append(x.rstrip())
                    # print('Recipient list:')
                    # print(recipient_list)

            elif '@' in args.rcpt:
                recipient_list = args.rcpt.lower().split(',')
                # print('Recipient list:')
                # print(recipient_list)

            else:
                print('\nUnsupported file format or email address.')
                print("Supported file types include: 'CSV' and 'TXT'.")
                print("Email addresses must be in the format: 'user@domain.com'")
                print('Separate multiple email addresses on the cli with a single comma')
        except IOError as e:
            errno, message = e.args
            if errno == 2:
                print('\n[!] Error: %s' % (message))

    # List availables email templates.
    if args.templates:
        print('Templates available:')
        for template in template_dic:
            print('[%s] %s' % (template, template_dic[template]))
        while True:
            try:
                template_choice = int(raw_input(
                    '\nSelect a template number to preview or "0" to exit:'))
                # User entered 0 and wants to quit.
                if template_choice == 0:
                    sys.exit(0)
                # Print selected email template contents
                selected_template = template_dic[template_choice]
                with open('templates/email/' + selected_template, 'r') as f:
                    for i in xrange(4):
                        f.next()
                    for template_line in f:
                        print(template_line.rstrip())
                continue
            except ValueError as e:
                message = e.args
                print("[!] Error: That's not an integer, please select again:")
                continue
            except KeyError as e:
                message = e.args
                print("[!] Error: Invalid selection: %s" % (message))
                continue
    # Configure email template for sending.
    elif args.template:
        create_email(recipient_list)
        # Preview written to active template
        print('\n')
        print('All recipients are shown in the message preview below.')
        print('Message Preview:')
        with open('templates/email/active_template.txt', 'r') as f:
            active_template = f.read()
            print(active_template)

    # Attempts to automatically determine SMTP relay.
    if not args.relay:
        if 'gmail.com' in args.user:
            args.relay = 'smtp.gmail.com'
            args.port = '587'
            args.mail_from = args.user
        elif 'outlook' in args.user:
            args.relay = 'smtp-mail.outlook.com'
            args.port = '587'
            arg.mail_from = args.user
        elif 'yahoo' in args.user:
            args.relay = 'smtp.mail.yahoo.com'
            args.port = '587'
            args.mail_from = args.user
        elif 'AT&T' in args.user:
            args.relay = 'smtp.mail.att.net'
            args.port = '465'
            args.mail_from = args.user
        elif 'comcast' in args.user:
            args.relay = 'smtp.comcast.net'
            args.port = '465'
            args.mail_from = args.user
        elif 'verizon' in args.user:
            args.relay = 'smtp.verizon.net'
            args.port = '465'
            args.mail_from = args.user

    # Config display
    print('\n')
    print('SMTP Server: %s' % (args.relay))
    print('Port: %s' % (args.port))
    print('User Account: %s' % (args.user))
    print('SMB Server: %s' % (args.smb_ip))
    # print('MAIL FROM: %s' % (args.mail_from))
    # print('RCPT TO: %s' % (recipient_list))
    print('Email Template: %s' % (args.template))
    print('Total number of recipients: %s' % (len(recipient_list)))

    if len(recipient_list) <= args.limit:
        args.limit = len(recipient_list)
    print('Number of recipients per batch: %s' % (args.limit))

    # Create recipient batch chunks.
    batch_number = 0
    chunks = [recipient_list[x:x + args.limit] for x in xrange(
        0, len(recipient_list), args.limit)]

    # Determine total number of batches.
    for batch_index, chunk in enumerate(chunks, start=1):
        batch_total = batch_index
        pass
    print('Total batches: %s' % (batch_total))
    print('Minutes delayed between each batch: %s' % (args.delay))

    print('\n')
    raw_input('Press <enter> to send messages!')

    # Define SMTP connector
    send_mail = smtpconnect

    for batch_list in chunks:
        batch_number += 1
        # Call create email function
        create_email(batch_list)
        # Preview written to active template
        # Borrowed from line 161  
        with open('templates/email/active_template.txt', 'r') as f:
            active_template = f.read()
        # Connect to SMTP relay.
        send_mail.SmtpConnect(
            args.relay, args.port, args.user, args.passwd,
            args.mail_from, batch_list, active_template)
        print('\nSent batch: %s of %s \nRecipient(s) %s ' % (batch_number, batch_total, batch_list))
        print('Next batch will send in %s minute(s)' % (args.delay))
        if batch_number != batch_total:
            time.sleep(delay)
        print('\n')
    sys.exit(0)
