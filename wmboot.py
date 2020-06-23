'''
Realy tiny script to reboot Wacom drivers
when they randomly decide to die under windows( really annoying btw, fix this pls WACOM )
'''
from subprocess import call

import ctypes, sys

service_name = 'WTabletServicePro'

def restart():
    call(['sc', 'stop', service_name])
    call(['sc', 'start', service_name])


# Now dont be scared...
# We need to elevate priveleges cause
# Restarting a service requires admin priveleges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if sys.platform not in {'win32', 'cygwin'}:
        print(f'WTF, bruh? Why you runnin this on non-windows machine? Get some sleep...')
        quit()
    if is_admin():
        restart()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
