#! /usr/bin/env python2

#coding: utf-8

__author__  = "CARLOS DIAZ | @DFIRENCE"
__credits__ = ("CERT-BDF")
__version__ = "0.0.1"
__license__ = 'MIT'

#   -- VERBOSE IMPORTS FOR NOW, MAKE IT CLEAR TO SEE SPECIFIC FUNCTIONS IMPORTED BY MODULE
#   -- REFACTOR ONCE ALL MODULES ARE RELEASED FOR NEXT VERSION

from sys import exit
from sys import argv
from sys import stdout
from os import devnull
from time import mktime
from time import sleep
from getpass import getuser
from datetime import datetime as dt

from menus import clear
from menus import animate
from menus import localsettings
from dbmodels import Case
from dbmodels import HiveCase
from dbmodels import SettingsDatabase
from dbmodels import LocalHostDatabase

#from templates.base.incident import render
from observables import upload_observables
from observables import process_observables

from modules.cliprompt import p9
#from modules.mailer import mailer
from modules.thehive.ttp0_thehive_api import TheHiveApi

import click


def normalize_ui_menu_op(T):
    '''
        Removes Extra Spaces From UI Menu Subcontext Menu
    '''
    if "  " in T[2][0]:
        return T[2][0].replace("  ", "")

    if "  " not in T[2][0]:
        return T[2][0]

def set_start_date_time():
    '''
        Creates a Time Structure Used by TheHive Case Mgmt System.
    '''
    now         = dt.now()
    secs_since  = mktime(now.timetuple()) + now.microsecond/1000000.0
    millisecs   = secs_since * 1000
    return millisecs

def prepare_security_incident_notification():
    ''' Structures User Input onto a standard format
        SIN = Security Incident Notification
        SIN data structure is customized by TTP0 as a
        python ordered dictionary from collections modules.
    '''
    ### --- Initiate an Incident From User Input
    incident = animate()

    ### --- Initiate a Case() Object
    case = Case()

    ### --- Prepare SOC User
    soc_user = getuser()
    case.sin['owner'] = soc_user

    ### -- Prepare Case Start Time
    case.sin['startDate'] = set_start_date_time()

    ### --- Prepare Case Status
    case.sin['status'] = 'Open'

    ### --- Prepare SubjectLine
    category        = incident[1][0].keys()[0].upper()
    casetype        = incident[1][0].values()[0]
    severity        = (incident[3][0], int(incident[3][1]))
    zone            = incident[4][0]
    tier            = incident[5][0].keys()[0]
    business_unit   = incident[6][0]
    subcontext      = normalize_ui_menu_op(incident)
    case.sin['subjectline'] = '[ {0} {1} {2} {3} ] {4} : {5} - {6}'.format(
        category,
        severity[0],
        zone,
        tier,
        business_unit,
        casetype,
        subcontext
    )

    ### --- Prepare Title
    case.sin['title'] = case.sin['subjectline'].upper()

    ### --- Prepare Tags - Standard
    master_tag = '{0}-{1}-{2}-{3}'.format(business_unit, zone, tier, severity[0])
    case.sin['tags'].extend([
        category,
        severity[0],
        zone,
        tier,
        business_unit,
        casetype.upper(),
        subcontext.upper(),
        master_tag,
        soc_user.upper()
    ])

    ### --- Prepare Severity
    case.sin['severity'] = severity[1]

    ### --- Prepare TLP
    case.sin['tlp'] = severity[1]

    return case

def prepare_hive_case(case):
    '''
        Returns a Python Dictionary with REST API Fields required by TheHive API
        HIVECASE is a python dictionary mapped to the REST API used by the CERT-BDF
        TheHive application.

        :param case:        A custom python dictionary aligned to the REST API Spec of a case
    '''
    return HiveCase(case)

def prepare_observables(case_input):
    '''
        Returns a Python List of Observable Datatags that are not empty
        which are used by the <process_observables> function to upload
        to TheHive REST API.

        :param case_input:      A custom python dictionary with python lists of observables
    '''
    non_empty_datatags = []
    for datatag in case_input:
        if len(case_input[datatag]) == 0:
            pass
        else:
            if datatag == 'analyst':
                pass
            else:
                non_empty_datatags.append(datatag)
    return non_empty_datatags

def configure_the_soc():
    '''
        Simple Interactive Menu for User to Customize their SOC Environment
        This configuration is stored under the "{PROJECT_FOLDER}/db" path
        as a json database used by the 3rd party TinyDB python library.
    '''
    hdr = '''

                                                   [ TTP0 | SOC CONFIGURATION MODE ]

            ---------------------------------------------------------------------------------------------------------------


            Interactice Helper to configure your Workflow


                - Organization Name         required    This is your Agency/Company/Organization Name

                - SOC Name                  required    This is your SOC/CIRT Designated Name

                - SOC Email                 required    This is your email distribution used in your SOC by clients

                - SOC URL for TheHive       required    This is your instance of TheHive

                - SOC APIKEY for TheHive    required    This is your APIKEY from TheHive Designated Account

                - SOC Total Zones           required    This is a number for the total number of zones you designed

                - Business Units            required    This is a number for te total number of business units you defend


            ---------------------------------------------------------------------------------------------------------------

    '''
    stdout.write(hdr)
    stdout.flush()
    mysoc = SettingsDatabase().configure()


def run_ops_mode():
    '''
        This calls the script and executes the current workflow.
        The script is not using the elasticsearch bulk apis at this time.
        The bulk apis are being tested and will be upgraded in future versions.
    '''
    localdb = LocalHostDatabase()

    sin = prepare_security_incident_notification()
    sin.sin['observables'] = p9.recordman.dedup
    clear()

    p9.main(sin.sin['title'])
    sin.sin['description'] = sin.sin['observables']['analyst']
    case = prepare_hive_case(sin)

    datatags = prepare_observables(sin.sin['observables'])

    settings = SettingsDatabase()
    restapi  = settings.load_settings()

    hiveapi  = TheHiveApi(restapi['soc_platform'], restapi['soc_apikey'])

    request = hiveapi.create_case(case.hivecase)
    sin.sin['restapi'] = {
        'caseId' : request['caseId'],
        'hiveId' : request['id'],
        'owner' : request['owner'],
        'title' : request['title']
    }

    caseid = sin.sin['restapi']['caseId']
    hiveid = sin.sin['restapi']['hiveId']

    process_observables(hiveapi, caseid, hiveid, sin, case, datatags)

    ##### EMAIL FOR WINDOWS PLATFORMS ONLY
    # LINUX PLATFORMS ARE WIP
    '''
    email_template = render(sin)
    try:
        sent = False
        mailer.create_message(to='YOUR_EMAIL_ADDRESS_LIST_HERE', incident=email_template)
        sent = True
        if sent:
            print '[+] Successful Email Security Incident Notification: {0}'.format(caseid)
    except Exception as e:
        print '[+] Email Sending <win32.com mailer>: {0}'.format(e)
    localdb.prepare(sin, request)
    localdb.insert(sin)
    return (sin, case, request)
    '''


@click.command()
@click.argument('mode')
def main(mode=None):
    '''
        Renders the workflow to the user.
    '''
    try:
        if mode == "configure":
            configure_the_soc()

        if mode == "run":
            if not localsettings:
                configure_the_soc()
            else:
                run_ops_mode()
                exit(0)

        if mode == "dryrun":
            incident = prepare_security_incident_notification()
            clear()
            p9.main(incident.sin['title'])
            exit(0)
    except KeyboardInterrupt:
        print "\n\n[!] Program Interrupted, exiting...\n\n"

def showUsageHelp():
    msg = '''
                        Program Usage:  ttp0_drone.py | v.{0}
    ---------------------------------------------------------------------------
    Example:
            $> ttp0_drone.py run
            $> ttp0_drone.py dryrun
            $> ttp0_drone.py configure

    Parameters:

            run         Run this program in live production mode
                        (Must have TheHive Running for this)

            dryrun      Run this program in test mode (No REST API)

            configure   Run the configuration mode (required)
                        You must run configure mode before you can
                        use the program in test or live mode

    --------------------------------------------------------------------------
    www.ttp0.io                                                   info@ttp0.io

    '''.format(__version__)
    print msg


if __name__ == "__main__":
    main()
