#coding: utf-8

__version__ = '0.01'
__author__  = '@DFIRENCE | CARLOS DIAZ'
__license__ = 'MIT'

from sys import exit
from sys import stdout
from json import loads
from os import path, getcwd, remove
from abc import ABCMeta, abstractmethod
from collections import OrderedDict as OD

from settings import Profile

try:
    from tinydb import TinyDB, Query
except ImportError:
    raise ImportError("Missing Dependency Package: TinyDB")
    exit(1)

class SettingsDatabase(Profile):
    '''Used to store the configured SOC Settings in a TinyDB JSON File.'''
    def configure(self):
        super(SettingsDatabase, self).configure()
        file = __file__
        abspath = path.abspath(file)
        dbp = path.join(path.dirname(abspath), 'db/soc_settings.json')
        with TinyDB(dbp) as database:
            self.conf['db'] = dbp
            database.insert(self.conf)
            stdout.write('\n\t\t[+] Settings Database Created in: {0}\n'.format(dbp))

    def load_settings(self):
        abspath = path.abspath(__file__)
        dbp = path.join(path.dirname(abspath), 'db/soc_settings.json')
        with open(dbp, 'rb') as database:
            config = loads(''.join(database.read()))
            valid = self.validate(config)
            return valid

    def validate(self, config):
        config = config['_default']

        if len(config.keys()) > 1:
            current = sorted(config.keys())[-1]
            return config[current]

        elif len(config.keys()) <= 1:
            return config['1']

        else:
            stdout.write('\n\t\t[!] Error:  No Settings Database Found')


#   ---     ABSTRACT FACTORY    ---
class Case(object):
    '''Abstract Object Used for the structure of SOC Incident/Case.'''
    def __init__(self):
        self.root = path.join(getcwd(), 'db')
        self.sin = OD()
        self.sin['tlp']         = ''
        self.sin['tags']        = ['autobot']
        self.sin['title']       = ''
        self.sin['owner']       = ''
        self.sin['status']      = ''
        self.sin['severity']    = ''
        self.sin['startDate']   = ''
        self.sin['subjectline'] = '[ {0} {1} {2} {3} ] {4} : {5}'
        self.sin['description'] = ''                                # Analyst Comments Here
        self.sin['observables'] = ''
        self.sin['hiverecords'] = OD()
    #@abstractmethod
    def insert(self):
        pass
#   ---

#   --- TheHive Case Structure
class HiveCase(Case):
    '''Class used to structure a SIN to upload via RESTAPI in TheHive Case Managment'''
    def __init__(self, case):
        self.hivecase               = OD()
        self.hivecase['tlp']        = 3 if case.sin['tlp'] == 4 else case.sin['tlp']
        self.hivecase['tags']       = case.sin['tags']
        self.hivecase['owner']      = case.sin['owner']
        self.hivecase['title']      = case.sin['title']
        self.hivecase['status']     = case.sin['status']
        self.hivecase['severity']   = 3 if case.sin['severity'] == 4 else case.sin['severity']
        self.hivecase['startDate']  = case.sin['startDate']
        self.hivecase['description'] = case.sin['description']

    def load_observable(self, item, datatag, caseid):
        datatag_mapping = {
            'urls': 'url',
            'fqdns': 'fqdn',
            'src_ip': 'ip',
            'dst_ip': 'ip',
            'hashes': 'hash',
            'src_email': 'other',
            'dst_email': 'other',
            #'email_subj' : 'other',
            'ldap_user': 'other',
            'ldap_host': 'other'
        }
        self.observable = OD()
        self.observable['tlp']      = self.hivecase['tlp']
        self.observable['tags']     = ['autobot', "CASE-{0}".format(caseid), datatag.upper(), self.hivecase['tags'][1]]
        self.observable['data']     = item
        self.observable['status']   = 'Ok'
        self.observable['message']  = self.hivecase['title']
        self.observable['dataType'] = datatag_mapping[datatag]
        self.observable['startDate'] = self.hivecase['startDate']

#   --- LocalHost Database Case Management Storage
class LocalHostDatabase(Case):
    '''Class used to create and store a local JSON database file with User Workflows.'''
    def __init__(self):
        super(LocalHostDatabase, self).__init__()
        self.root = path.join(self.root, 'local_hostdb.json')

    def prepare(self, sin, hiveresponse):
        hivecontent= loads(hiveresponse.content)
        if hiveresponse.status_code == 201:
            sin.sin['subjectline'] = sin.sin['subjectline'] + " | SIN # {0}".format(hivecontent['caseId'])
            sin.sin['hiverecord'] = OD()
            sin.sin['hiverecord']['db_id']   = hivecontent['id']
            sin.sin['hiverecord']['caseid']  = hivecontent['caseId']
            sin.sin['hiverecord']['creator'] = hivecontent['createdBy']

        else:
            stdout.write('\n\n[+] Warning:  HiveCase Creation did not work')

    def insert(self, sin):
        with TinyDB(self.root) as database:
            database.insert(sin.sin)
