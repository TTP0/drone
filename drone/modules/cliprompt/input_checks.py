#coding: utf-8

__author__  = "@DFIRENCE | CARLOS DIAZ"
__version__ = "0.0.1"
__license__ = "MIT"

import re
from textwrap import wrap
from collections import OrderedDict as OD

from colors import Palette

colors = Palette()

comma    = ','
space    = ' '
newline  = '\n'
nullchar = ''

### --- TRUTHY TABLE PATTERNS
split_newlines                  = [False, False, True]
split_newlines_spaces           = [False, True, True]
split_newlines_spaces_commas    = [True, True, True]
split_spaces                    = [False, True, False]
split_spaces_commas             = [True, True, False]
split_commas                    = [True, False, False]
split_commas_newlines           = [True, False, True]
no_split_single_value           = [False, False, False]
### ---

stream_patterns = [
    split_newlines,                 # 0 - Newlines  Split Newlines
    split_newlines_spaces,          # 1 - Newlines  Split Newlines & Spaces
    split_newlines_spaces_commas,   # 2 - Newlines  Split Newlines & Spaces & Commas
    split_spaces,                   # 3 - Spaces    Split Spaces
    split_spaces_commas,            # 4 - Spaces    Split Spaces & Commas
    split_commas,                   # 5 - Commas    Split Commas
    split_commas_newlines,          # 6 - Commas    Split Commas & Newlines
    no_split_single_value           # 7 - Single    Single Item
]

### TODO: IN FUTURE
'''
In [4]: def remove_by_index(theset, index_value):
   ...:     if isinstance(theset, set):
   ...:         theset.discard(index_value)
'''
### ENSURE THIS ORDERED DICT MATCHES THE DBMODELS.PY
class RecordManager(object):
    def __init__(self):
        self.uniq  = set()
        self.dedup = OD()
        self.dedup['urls']      = set()
        self.dedup['fqdns']     = set()
        self.dedup['src_ip']    = set()
        self.dedup['dst_ip']    = set()
        self.dedup['hashes']    = set()
        self.dedup['analyst']   = ''
        self.dedup['src_email'] = set()
        self.dedup['dst_email'] = set()
        self.dedup['ldap_user'] = set()
        #self.dedup['email_subj'] = set()
        self.dedup['useragents'] = set()
        #self.dedup['ldap_host'] = set() #TO DO


### --- DATA VALIDATION METHODS
    def validate_remove_by_index(self, item):
        num_seq = r'^\d{1,9}'
        pattern = re.compile(num_seq)
        if pattern.search(item):
            return True     # Good Numeric Option
        else:
            return False    # Bad Numeric Option

    def validate_email_address(self, item):
        email_address = r'.*@.*\.'
        pattern = re.compile(email_address)
        if pattern.search(item):
            return True     # GOOD EMAIL ADDRESS
        else:
            return False    # BAD EMAIL ADDRESS

    def validate_hash(self, item):
        sha256  = r'^[a-f0-9]{64}$'
        sha1    = r'^[a-f0-9]{40}$'
        md5     = r'^[a-f0-9]{32}$'
        patterns = (
            re.compile(sha256),
            re.compile(sha1),
            re.compile(md5)
        )
        for hash_pattern in patterns:
            if hash_pattern.search(item.lower()):
                return True     # GOOD HASH
            else:
                pass
        else:
            return False        # BAD HASH

    def validate_ip_address(self, item):
        ipaddr  = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        bad     = r'[3-9]{3}|[3-9]\d{2}|\.0{2,}|^0{1,3}\.|\d{4,}|\.0$|^0\d{1,2}\.|\.0\d{1,2}|^\.|\.$'
        base_ip = re.compile(ipaddr)
        bad_ip  = re.compile(bad)
        if base_ip.search(item):
            if bad_ip.search(item):
                return False    # BAD IP
            else:
                return True     # GOOD IP

    def validate_url(self, item):
        url_pattern = r'(^http://|^https://|^ftp://|^file://|^h.*://|.*://)'
        base_urls   = re.compile(url_pattern)
        if base_urls.search(item):
            return True     # GOOD URL
        else:
            return False    # BAD URL


### --- SAVE METHODS
    def save_url(self, urlset, datatag=None):
        if isinstance(urlset, set):
            for elem in urlset:
                if self.validate_url(elem):
                    elem = elem.lower()
                    self.dedup[datatag].update([elem])
                else:
                    pass
            sorted(self.dedup[datatag])
            return True

    def save_ip(self, ipset, datatag=None):
        if isinstance(ipset, set):
            for elem in ipset:
                if self.validate_ip_address(elem):
                    elem = elem.lower()
                    self.dedup[datatag].update([elem])
                else:
                    pass
            return True

        if not isinstance(ipset, set):
            msg = '(-) WARNING ERROR:  You must pass a Python Set to Save IP Address List'
            print msg
            return False

    def save_hash(self, hashset, datatag=None):
        if isinstance(hashset, set):
            for elem in hashset:
                if self.validate_hash(elem):
                    elem = elem.lower()
                    self.dedup[datatag].update([elem])
                else:
                    pass
                    #print "(-) BAD Hash: {}".format(elem)
            return True

    def save_analyst_comments(self, input, datatag=None):
        if input == '.' or input == ',' or input == '':
            pass
        else:
            content = ' '.join(input.split('\n'))
            self.dedup[datatag] = content

    def save_fqdns(self, fqdns_set, datatag=None):
        if isinstance(fqdns_set, set):
            for elem in fqdns_set:
                elem = elem.lower()
                self.dedup[datatag].update([elem])
            return True

    def save_ldap_users(self, ldap_user_set, datatag=None):
        if isinstance(ldap_user_set, set):
            for elem in ldap_user_set:
                elem = elem.lower()
                self.dedup[datatag].update([elem])
            return True

    def save_email_address(self, email_set, datatag=None):
        if isinstance(email_set, set):
            for elem in email_set:
                if self.validate_email_address(elem):
                    elem = elem.lower()
                    self.dedup[datatag].update([elem])
                else:
                    pass
            return True

    def save_email_subjectlines(self, email_subj_set, datatag=None):
        if isinstance(email_subj_set, set):
            for elem in email_subj_set:
                self.dedup[datatag].update([elem])
            return True

### --- DATA REMOVAL METHODS
    def remove_from_set_by_index(self, index_num, theset):
        if isinstance(theset, set):
            theset.discard(index_num)
            return True

    def remove_from_set(self, item, theset):
        if isinstance(item, list) and len(item) == 1:
            print newline
            if item[0] in theset:
                theset.remove(item[0])
                print '[+] Deleted Item: {0}'.format(item[0])
                print newline
                return True

        if isinstance(item, list) and len(item) > 1:
            print newline
            for elem in item:
                if elem in theset:
                    theset.remove(elem)
                    print '[+] Deleted Item: {0}'.format(elem)
            print newline
            return True

        if item in theset:
            theset.remove(item)
            print '[+] Deleted Item: {0}'.format(item)
            return True

        else:
            print '\n(-) Item Not Found: {0}\n'.format(item)
            return False

### --- INPUT VALIDATION METHODS
    def check_delims(self, stream):
        self.flags = []
        if comma in stream:
            self.flags.append(True) # Comma == Position 0
        else:
            self.flags.append(False)

        if space in stream:
            self.flags.append(True) # Space == Position 1
        else:
            self.flags.append(False)

        if newline in stream:
            self.flags.append(True) # Newline == Position 2
        else:
            self.flags.append(False)

    def remove_item(self, item):
        self.uniq.remove(item)

    def check_stream_patterns(self, flag_patterns, stream):
        for index, pattern in enumerate(stream_patterns):
            if pattern == flag_patterns:
                # AUTO CHOOSE CORRECT PATTERN AND PARSE
                # PARSER NEEDS TO AUTO UPDATE <SELF.UNIQ> PYTHON SET WHEN DONE
                if index == 0:
                    self.clean_newlines(stream)
                elif index == 1:
                    self.clean_newlines_spaces(stream)
                elif index == 2:
                    self.clean_newlines_spaces_commas(stream)
                elif index == 3:
                    self.clean_spaces(stream)
                elif index == 4:
                    self.clean_spaces_commas(stream)
                elif index == 5:
                    self.clean_commas(stream)
                elif index == 6:
                    self.clean_commas_newlines(stream)
                elif index == 7:
                    self.uniq.update([stream])
                else:
                    print "[!] WARNING: INPUT Pattern Not Recognized"
            else:
                pass

    def clean_newlines(self, stream):
        content = stream.split(newline)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

    def clean_newlines_spaces(self, stream):
        content = stream.split(newline)
        content = ' '.join(content).split(space)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

    def clean_newlines_spaces_commas(self, stream):
        content = stream.split(newline)
        content = ' '.join(content).split(space)
        content = ','.join(content).split(comma)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

    def clean_spaces(self, stream):
        content = stream.split(space)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

    def clean_spaces_commas(self, stream):
        content = stream.split(space)
        content = ','.join(content).split(comma)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

    def clean_commas(self, stream):
        content = stream.split(comma)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

    def clean_commas_newlines(self, stream):
        content = stream.split(newline)
        content = ','.join(content).split(comma)
        for item in content:
            if item == nullchar:
                pass
            else:
                self.uniq.update([item])

### --- PRETTY OUTPUT METHODS
    def show_values(self, datatag):
        table_header = ("Index", "Values", "Type", "Status")
        dash_header  = (
            "-" * 7,
            "-" * 32,
            "-" * 10,
            "-" * 14
        )
        view_columns = "{:>7}\t\t{:>32}\t{:>10}{:>32}".format(*table_header)
        view_dashes  = "{:>7}\t\t{:>32}\t{:>10}{:>32}".format(*dash_header)
        view_items   = "{:>7}\t\t{:>32}\t{:>10}{:>32}"

        print colors.color['white'] + "{0}{1}".format("\n\n", view_columns)
        print view_dashes

        for idx, elem in enumerate(sorted(self.dedup[datatag])):
            print view_items.format(idx, elem, datatag, "Upload Pending")
        print "{0}".format("\n")

    def show_values_hashes(self, datatag):
        table_header = ("Index", "Values", "Type", "Hash Type", "Status")
        dash_header  = (
            "-" * 7,
            "-" * 64,
            '-' * 10,
            "-" * 10,
            "-" * 14
        )
        view_columns = "{:>7}\t\t{:>64}\t{:>10}\t{:>10}{:>32}".format(*table_header)
        view_dashes  = "{:>7}\t\t{:>64}\t{:>10}\t{:>10}{:>32}".format(*dash_header)
        view_items   = "{:>7}\t\t{:>64}\t{:>10}\t{:>10}{:>32}"
        print colors.color['white'] + "{0}{1}".format("\n\n", view_columns)
        print view_dashes
        hash_type = ''
        for idx, elem in enumerate(sorted(self.dedup[datatag])):
            if len(elem) == 64:
                hash_type = "sha-256".upper()
            elif len(elem) == 40:
                hash_type = "sha-1".upper()
            elif len(elem) == 32:
                hash_type = "md5".upper()
            print view_items.format(idx, elem.upper(), datatag, hash_type, "Upload Pending")
        print "{0}".format("\n")


    def show_values_urls(self, datatag):
        table_header = ("Index", "Values", "Type", "Status")
        dash_header  = (
            "-" * 7,
            "-" * 64,
            "-" * 10,
            "-" * 14
        )
        view_columns = "{:>7}\t\t{:^64}\t{:>10}{:>32}".format(*table_header)
        view_dashes  = "{:>7}\t\t{:>64}\t{:>10}{:>32}".format(*dash_header)
        view_items   = "{:>7}\t\t{:>64}\t{:>10}{:>32}"
        print colors.color['white'] + "{0}{1}".format("\n\n", view_columns)
        print view_dashes
        for idx, elem in enumerate(self.dedup[datatag]):
            if len(elem) > 64:
                for iter, chunk in enumerate(wrap(elem, width=64)):     # WRAP TEXT LINES INTO 64 CHARS
                        if iter == 0:
                            print view_items.format(idx, chunk, datatag, "Upload Pending")
                        else:
                            print view_items.format('', chunk, '', '')
                print "\n"
            else:
                print view_items.format(idx, elem, datatag, "Upload Pending") + "\n"
        print "{0}".format("\n")


    def show_values_fqdns(self, datatag):
        table_header = ("Index", "Values", "Type", "Status")
        dash_header  = (
            "-" * 7,
            "-" * 64,
            "-" * 10,
            "-" * 14
        )
        view_columns = "{:>7}\t\t{:^64}\t{:>10}{:>32}".format(*table_header)
        view_dashes  = "{:>7}\t\t{:>64}\t{:>10}{:>32}".format(*dash_header)
        view_items   = "{:>7}\t\t{:>64}\t{:>10}{:>32}"
        print colors.color['white'] + "{0}{1}".format("\n\n", view_columns)
        print view_dashes
        for idx, elem in enumerate(self.dedup[datatag]):
            if len(elem) > 64:
                # If String Length is > 64, we use the Python WRAP Module
                for iter, chunk in enumerate(wrap(elem, width=64)):     # WRAP TEXT LINES INTO 64 CHARS
                        if iter == 0:
                            print view_items.format(idx, chunk, datatag, "Upload Pending")
                        else:
                            print view_items.format('', chunk, '', '')
                print "\n"
            else:
                print view_items.format(idx, elem, datatag, "Upload Pending") + "\n"
        print "{0}".format("\n")
