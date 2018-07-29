#coding: utf-8

__author__  = "@DFIRENCE | CARLOS DIAZ"
__version__ = "0.0.1"
__license__ = "MIT"

import sys
from platform import platform

os_type = platform()

if "win" in os_type.lower():
    try:
        import win32com
    except ImportError:
        print "         Dependency Needed: Win32Com Not Installed"
        print "         Try to install Win32Com or disable email services for this script"
        print "         Disable Lines as covered in the github wiki"
        sys.exit(1)



def load_outlook():
    outlook = win32com.client.Dispatch( 'Outlook.Application' )
    message = outlook.CreateItem( 0x0 )
    return message


def create_message( to='', cc='', bcc='', html='', incident='' ):
    message = load_outlook()
    message.To       = to
    message.CC      = cc
    message.HTMLBody = incident.sin['template']
    message.Subject  = incident.sin['title'] + " | CIRT {0}".format(incident.sin['restapi']['caseId'])
    message.Send()
    return
