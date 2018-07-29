#coding: utf-8

from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter

from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

from input_checks import RecordManager

# Prompt Style
prompt_style = style_from_dict({
    # User input.
    Token:              '#ff0066',

    # Prompt.
    Token.Observables:  '#b2b2b2 italic',
    Token.Pipe:         '#00ffff', # cyan
    Token.Dash:         '#00ffff',
    Token.Criteria:     '#ffffff', # White
    Token.Symbol:       '#00ffff',

    # Toolbar - Bottom
    Token.Toolbar:      '#ffffff bg:#333333',
    # Make a selection reverse/underlined.
    # (Use Control-Space to select.)
    Token.SelectedText: 'reverse underline',

})

command_completer = WordCompleter(['done','remove','reset','show','skip'])
command_history = InMemoryHistory()


#   --- CLIPROMPT   TOKENS
def tokens_src_ip(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('IPv4 Sources')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_dst_ip(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('IPv4 Destinations')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_fqdns(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('FQDN Destinations')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_urls(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('URLs')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]


def tokens_useragents(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('User-Agents')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_hashes(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('File Hashes')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_ldap_users(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('LDAP Usernames')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_src_email(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('Email Senders')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]

def tokens_dst_email(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('Email Recipients')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]
'''
def tokens_email_subjectlines(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('Email Subjectlines')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]
'''
def tokens_analyst_comments(cli):
    return [
        (Token.Observables, 'Observables '),
        (Token.Pipe,        '|'),
        (Token.Dash,        '-'),
        (Token.Criteria,    '{:<20}'.format('Analyst Comments')),
        (Token.Symbol,      '{:>2}'.format('> '))
    ]
#   ---

#   --- MINI TERMINALS
class PromptTokens(object):
    def __init__(self):
        self.cli = {
            'src_ip'    : tokens_src_ip     ,
            'dst_ip'    : tokens_dst_ip     ,
            'fqdns'     : tokens_fqdns      ,
            'urls'      : tokens_urls       ,
            'useragents': tokens_useragents ,
            'hashes'    : tokens_hashes     ,
            'ldap_user' : tokens_ldap_users ,
            'src_email' : tokens_src_email  ,
            'dst_email' : tokens_dst_email  ,
            #'email_subj': tokens_email_subjectlines,
            'analyst'   : tokens_analyst_comments
        }
#   ---

cliprompt = PromptTokens()
recordman = RecordManager()

recordentry = {
    'src_ip'    : recordman.save_ip,
    'dst_ip'    : recordman.save_ip,
    'fqdns'     : recordman.save_fqdns,
    'urls'      : recordman.save_url,
    #'useragents': #ToDo
    'hashes'    : recordman.save_hash,
    'ldap_user' : recordman.save_ldap_users,
    'src_email' : recordman.save_email_address,
    'dst_email' : recordman.save_email_address,
    #'email_subj': recordman.save_email_subjectlines,
    'analyst'   : recordman.save_analyst_comments
}

showitems = {
    'src_ip'    : recordman.show_values,
    'dst_ip'    : recordman.show_values,
    'fqdns'     : recordman.show_values_fqdns,
    'urls'      : recordman.show_values_urls,
    'hashes'    : recordman.show_values_hashes,
    'ldap_user' : recordman.show_values,
    'src_email' : recordman.show_values,
    'dst_email' : recordman.show_values,
    #'email_subj': recordman.show_values
    #'analyst'   : N/A
}
datatags = [
    'src_ip'    ,
    'dst_ip'    ,
    'fqdns'     ,
    'urls'      ,
#    'useragents',      # <- ToDom need cli prompt
    'hashes'    ,
    'ldap_user' ,
    #'ldap_host' ,      # <- ToDo, need cli prompt
    'src_email' ,
    'dst_email' ,
    #'email_subj',
    'analyst'
]

def enable_cliprompt(datatag, title):
    '''
        Provides the visual rendering of each observable sectiona
        based on datatags dictionary.
        :param: datatag     this is the observable datatag in the queue
        :param: title       This is the name of the SIN title
    '''
    def tokens_bottom_toolbar(cli):
        return [(Token.Toolbar, title)]

    if datatag == 'analyst':
        return prompt(
            get_bottom_toolbar_tokens=tokens_bottom_toolbar,
            get_prompt_tokens=cliprompt.cli[datatag],
            history=command_history,
            style=prompt_style,
            wrap_lines=True,
            multiline=True
        )
    else:
        return prompt(
            get_bottom_toolbar_tokens=tokens_bottom_toolbar,
            get_prompt_tokens=cliprompt.cli[datatag],
            completer=command_completer,
            history=command_history,
            style=prompt_style
        )

def main(title):
    skipped = False
    not_done = True
    saved_items = '\n[+] Saved Items: {0}\n'

    #   --- CORE LOOP OF SHELL ENTRIES CODE BLOCK
    for tag in datatags:
        if skipped:
            break

        while not_done:
            text = enable_cliprompt(tag, title)

            if text in command_completer.words:
                #   --- BUILT-IN COMMANDS CODE BLOCK
                if text == 'skip':
                    tag = 'analyst'
                    text = enable_cliprompt(tag, title)
                    recordentry[tag](text, datatag=tag)
                    skipped = True
                    break

                if text == 'done':
                    if recordentry[tag](recordman.uniq, datatag=tag):
                        recordman.uniq.clear()
                        if len(recordman.dedup[tag]) > 1:
                            print '\t{0}'.format(saved_items.format(len(recordman.dedup[tag])))
                        break

                if text == 'reset':
                    recordman.dedup[tag].clear()

                if text == 'show':
                    showitems[tag](tag)
            else:
                #   --- SAVE/DONE CODE BLOCK
                if text == '.':
                    if recordentry[tag](recordman.uniq, datatag=tag):
                        recordman.uniq.clear()
                        if len(recordman.dedup[tag]) > 1:
                            print '\t{0}'.format(saved_items.format(len(recordman.dedup[tag])))
                    break

                #   --- NULL/NONE USER INPUT CODE BLOCK
                if text == '':
                    pass

                #   --- REMOVE ITEM INPUT CODE BLOCK
                if text.startswith('remove'):
                    content = text.split(' ')[1:]
                    recordman.remove_from_set(content, recordman.dedup[tag])

                else:
                    #   --- USER INPUT VALIDATION CODE BLOCK
                    recordman.check_delims(text)
                    recordman.check_stream_patterns(recordman.flags, text)

                    #   --- MULTI LINE USER INPUT CODE BLOCK
                    if tag == 'analyst':
                        recordentry[tag](text, datatag=tag)
                        break
                    else:
                        if recordentry[tag](recordman.uniq, datatag=tag):
                            recordman.uniq.clear()



    #print recordman.dedup



if __name__ == '__main__':
    title = 'SIMULATION'
    main(title)
