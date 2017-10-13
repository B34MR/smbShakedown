#!/usr/bin/env python
# Script: smbShakedown 2.0
# Description: SMB Email Client Attack script.
# Author(s): Nick Sanzotta / @beamr
# Version: v 2.09302017
try:
    import sys
    import core
except Exception as e:
    print('[!] SMBSHAKEDOWN - Error: %s' % (e))
    sys.exit(1)


def run():
    core.main()

if __name__ == '__main__':
    run()
