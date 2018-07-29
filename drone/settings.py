#coding: utf-8

__author__  = "@DFIRENCE | CARLOS DIAZ"
__version__ = "0.0.1"
__license__ = "MIT"

import time
from os import path, getcwd
from datetime import datetime
from abc import ABCMeta, abstractmethod
from collections import OrderedDict as OD


#   --- ABSTRACT CLASS  ---
class Settings(object):
    ''' Root Settings Object Used for Inheritance. '''
    __metaclass__ = ABCMeta
    def __init__(self):
        self.conf = OD({
            'db':           '',
            'tlp':          '',
            'email':        '',
            'zones':        '',
            'tiers':        '',
            'severity':     '',
            'framework':    '',
            'subcontext':   '',
            'organization': '',
            'configured_date': OD({
                'timezone': time.tzname,
                'datetime': datetime.now().isoformat()
            })
        })

    @abstractmethod
    def configure(self):
        pass
#   ---


class Profile(Settings):
    ''' Configure the Profile of the SOC Based on Guided User Input.'''
    def ask(self):
        msg = {
            'org':              '\t\t[setup] Organization Name            :   ',
            'email':            '\t\t[setup] SOC Email                    :   ',
            'name':             '\t\t[setup] SOC Name                     :   ',
            'zones':            '\t\t[setup] SOC Zones Total Number       :   ',
            'system':           '\t\t[setup] URL of TheHive <http|https>  :   ',
            'apikey':           '\t\t[setup] APIKEY of TheHive            :   ',
            'internal_orgs':    '\t\t[setup] Business Units Total Number  :   '
        }

        #   Required User Inputs applied to Settings Database
        orgname     = raw_input(msg['org'])
        socname     = raw_input(msg['name'])
        email       = raw_input(msg['email'])
        platform    = raw_input(msg['system'])
        soc_apikey  = raw_input(msg['apikey'])
        num_zones   = raw_input(msg['zones'])
        num_business_orgs   = raw_input(msg['internal_orgs'])

        #   Return User Inputs as a Python Tuple Object
        return (email, socname, int(num_zones), platform, int(num_business_orgs), orgname, soc_apikey)

    def configure(self):
        props = self.ask()
        self.conf['org']            = props[5]
        self.conf['tlp']            = self.load_tlp()
        self.conf['zones']          = self.load_zones(props[2])
        self.conf['tiers']          = self.load_tiers()
        self.conf['email']          = props[0].upper()
        self.conf['severity']       = self.load_severity()
        self.conf['framework']      = self.load_framework()
        self.conf['subcontext']     = self.load_subcontext()
        self.conf['organization']   = props[1].upper()
        self.conf['soc_platform']   = props[3]
        self.conf['soc_apikey']     = props[6]
        self.conf['business_orgs']  = self.load_business_units(props[4])

    def load_tlp(self):
        tlp = OD()
        tlp[0] = 'WHITE'
        tlp[1] = 'GREEN'
        tlp[2] = 'AMBER'
        tlp[3] = 'RED'
        return tlp

    def load_zones(self, num_zones):
        zonemap = OD()
        print ""
        for n in xrange(1, num_zones + 1):
            zone = raw_input('\t\t[setup] SOC Zone {0}                   :   '.format(str(n)))
            zonemap[n] = zone.upper()
        return zonemap

    def load_business_units(self, num_business_orgs):
        orgs = OD()
        print ""
        for n in xrange(1, num_business_orgs + 1):
            org = raw_input('\t\t[setup] SOC Business Unit {0}          :   '.format(str(n)))
            orgs[n] = org.upper()
        orgs[n+1] = "VARIOUS";
        return orgs

    def load_tiers(self):
        tier = OD()
        tier[1] = OD({'T1' : 'User Devices'})
        tier[2] = OD({'T2' : 'Infrastructure Devices'})
        tier[3] = OD({'T3' : 'Critical Devices'})
        return tier

    def load_severity(self):
        sev = OD()
        sev[1] = 'LOW'
        sev[2] = 'MEDIUM'
        sev[3] = 'HIGH'
        sev[4] = 'CRITICAL'
        return sev

    def load_framework(self):
        fr = OD()
        fr[0] = OD({'cat0' : 'Simulation'})
        fr[1] = OD({'cat1' : 'Intrusion'})
        fr[2] = OD({'cat2' : 'Dos/DDoS'})
        fr[3] = OD({'cat3' : 'Malware'})
        fr[4] = OD({'cat4' : 'Violation'})
        fr[5] = OD({'cat5' : 'Probing'})
        fr[6] = OD({'cat6' : 'Unknown'})
        fr[7] = OD({'cat7' : 'Countermeasure'}) # <- Threat Countermeasure
        fr[8] = OD({'cat8' : 'Forensics'})
        fr[9] = OD({'cat9' : 'False Positive'})
        return fr

    def load_subcontext(self):
        sc = OD()
        sc['cat0'] = OD({
            1 : 'PENTEST',
            2 : 'TTOP - TableTop',
            3 : 'Adversary Emulation'
        })

        sc['cat1'] = OD({
            1 : 'Malware Aftermath',
            2 : 'Exploit Aftermath',
            3 : 'Theft',
            4 : 'Vendor Compromise',
            5 : 'Account Compromise',
            6 : 'Insider Threat Aftermath',
            7 : 'Phishing'

        })
        sc['cat2'] = OD({
            1 : 'Volumetric',
            2 : 'Reflective',
            3 : 'Amplified',
            4 : 'Backscatter'
        })
        sc['cat3'] = OD({
            1 : 'Dropper',
            2 : 'Downloader',
            3 : 'RootKit',
            4 : 'Exploit',
            5 : 'WebShell',
            6 : 'PUP-Riskware',
            7 : 'Ransomware',
            8 : 'Virus',
            9 : 'Worm',
            10 : 'Trojan/RAT',
            11 : 'C2 Callbacks'
        })
        sc['cat4'] = OD({
            1 : 'Unsafe         Security Protection Status',
            2 : 'Unsafe         Patching Status',
            3 : 'Unsafe         Web Browsing',
            4 : 'Unsafe         Privilege Use',
            5 : 'Unsafe         Configuration Status',
            6 : 'Unauthorized   Data Handling',
            7 : 'Unauthorized   Security Changes',
            8 : 'Unauthorized   Rogue System',
            9 : 'Unauthorized   Copyright Access',
            10 : 'Unauthorized   Privilege Use'
        })
        sc['cat5'] = OD({
            1 : 'User Enumeration',
            2 : 'Port Enumeration',
            3 : 'Attempted WebApp Probing',
            4 : 'Attempted Email Phishing',
            5 : 'Attempted CVE Exploitation',
            6 : 'Attempted SQL Injection',
            7 : 'Attempted XSS Injection',
            8 : 'Attempted UDP/TCP/IP Protocol Abuse'
        })
        sc['cat6'] = OD({
            1 : 'Abnormal Outage',
            2 : 'Abnormal Server Activity',
            3 : 'Abnormal UDP/TCP/IP Connections',
            4 : 'Abnormal User Report',
            5 : 'Abnormal User Password Resets',
            6 : 'Abnormal Data Transfer Volume(s)',
            7 : 'Abnormal System Reboot(s)'
        })
        sc['cat7'] = OD({
            1 : 'Endpoint',
            2 : 'Firewall',
            3 : 'Proxy',
            4 : 'SIEM',
            5 : 'O365/Email',
            6 : 'IDS - Intrusion Detection',
            7 : 'IPS - Intrusion Prevention',
            8 : 'WAF - Web Application Firewall',
            9 : 'IDM - Identity Management Provider',
            10 : 'GPO - Group Policy Objects',
            11 : 'Vulnerability Port Scan',
            12 : 'Authenticated Vulnerability Scan',
            13 : 'Enhanced Security Logging'
        })
        sc['cat8'] = OD({
            1 : 'Forensics - Malware Code',
            2 : 'Forensics - E-Discovery',
            3 : 'Forensics - Insider Threat',
            4 : 'Forensics - Fraudulent Threat',
            5 : 'ThreatIntel - Adversary Synthesis',
            6 : 'ThreatIntel - Industry Synthesis',
            7 : 'ThreatIntel - APT Synthesis',
            8 : 'ThreatIntel - KillChain Synthesis',
        })
        sc['cat9'] = OD({
            1 : 'Approved Activity',
            2 : 'Bad IoC/IoA',
            3 : 'Explained Anomaly',
            4 : 'User Error'
        })
        return sc
