#coding: utf-8

__author__  = "@DFIRENCE | CARLOS DIAZ"
__version__ = "0.0.1"
__license__ = "MIT"

import re
import sys
from time import sleep
from os import system
from platform import platform

from dbmodels import SettingsDatabase
from colors import Palette


special = re.compile(r"(!|@|#|\$|%|\^|&|\*|\(|\)|-|_|\+|=|\{|\}|\[|\]|;|:|'|\"|`|~|<|>|\?|,|\.|/)")
alpha   = re.compile(r"(A|C|D|E|F|G|H|I|J|K|L|M|N|O|P|R|S|T|U|V|W|X|Y|Z|a|c|d|e|f|g|h|i|j|k|l|m|n|o|p|r|s|t|u|v|w|x|y|z){1,}")
colors = Palette()


def clear():
    ostype = platform()
    if 'linux' in ostype.lower():
        system('clear')
    elif 'windows' in ostype.lower():
        system('cls')
    else:
        system('clear')


try:
    settings = SettingsDatabase()
    settings = settings.load_settings()
    localsettings = True
except IOError as e:
    localsettings = False
    msg = '''
                   [!] WARNING - SETTINGS DATABASE NOT FOUND
        --------------------------------------------------------------
        help message:
            You are being routed to the Interactive Configuration Mode

    '''
    sys.stdout.write(msg)
    sys.stdout.flush()
    sleep(3)
    clear()

#   ---     INCIDENT OPTIONS MENU   ---
def validate_incident_choice(framework, choice_num, count):
    msg = '\n\t\t[?] Error: You must choose a number between 0 and %s\n' % (count - 1)
    if choice_num == '' or special.search(choice_num):
        clear()
        print colors.color['red'] + msg
        return False

    if alpha.search(choice_num):
        clear()
        print colors.color['red'] + msg
        return False

    if choice_num == 'B'.lower() or choice_num == 'b'.upper():
        clear()
        return 'B'.lower()

    if choice_num == 'Q'.lower() or choice_num == 'q'.upper():
        clear()
        sys.exit()

    if not int(choice_num) < 0 and int(choice_num) <= count - 1:
            return (framework[choice_num], choice_num)

    else:
        clear()
        msg = '\n\t\t[?] Error: You must choose a number between 0 and %s\n' % (count - 1)
        print colors.color['red'] + msg
        return False


def validate_choice(framework, choice_num, count):
    msg = '\n\t\t[?] Error: You must choose a number between 0 and %s\n' % (count - 1)
    if choice_num == '' or special.search(choice_num):
        clear()
        print colors.color['red'] + msg
        return False

    if alpha.search(choice_num):
        clear()
        print colors.color['red'] + msg
        return False

    if choice_num == 'B'.lower() or choice_num == 'b'.upper():
        clear()
        return 'B'.lower()

    if choice_num == 'Q'.lower() or choice_num == 'q'.upper():
        clear()
        sys.exit()

    if not int(choice_num) <= 0 and int(choice_num) <= count:
        return (framework[choice_num], choice_num)

    else:
        clear()
        msg = '\n\t\t[?] Error: You must choose a number between 1 and %s\n' % (count)
        print colors.color['red'] + msg
        return False


def show_incident_types():
    sys.stdout.write('\n\t\t               ')
    sys.stdout.write(colors.color['cyan'] + '[ ')
    sys.stdout.write(colors.color['white'] + 'INCIDENT CATEGORY TYPES')
    sys.stdout.write(colors.color['cyan'] + ' ]')
    sys.stdout.write('               \n\n')
    sys.stdout.flush()
    framework = settings['framework']
    count = 0
    for n in sorted(framework.keys()):
        count += 1
        for k,v in framework[n].iteritems():
            sys.stdout.write(colors.color['white'] + '\t\t{0}'.format(n))
            sys.stdout.write(colors.color['cyan'] + ' -')
            sys.stdout.write(colors.color['grey'] + '  {0}  {1}\n'.format(k.upper(), v))
    back = '\n\t\t{0}\n'.format('Press "Q" and ENTER to go exit program')
    sys.stdout.write(back)
    sys.stdout.flush()

    msg  = colors.color['white'] + '\n\t\t{0} >  '.format('Select Incident Type')
    choice = raw_input(msg)

    valid = validate_incident_choice(framework, choice, count)

    if valid == 'B'.lower():
        return 'B'.lower()

    if isinstance(valid, tuple):
        return valid

    else:
        retry = show_incident_types()
        return retry


def show_subcontext_header(context):
    msg = '\n\t\t---------------[ {0} {1} CONTEXT ]---------------\n\n'
    msg = '\n\t\t              '
    hdr = '{0} {1} CONTEXT'
    sys.stdout.write(msg)
    sys.stdout.write(colors.color['cyan'] + '[ ')
    for k,v in context.iteritems():
        sys.stdout.write(colors.color['white'] + hdr.format(k.upper(), v.upper()))
        sys.stdout.write(colors.color['cyan'] + ' ]')
        sys.stdout.write('\n\n')
        sys.stdout.flush()

def show_incident_subcontext(choice):
    previous = choice[0].keys()[0].upper()
    show_subcontext_header(choice[0])
    category = '{0}{1}'.format('cat', choice[1])
    framework = settings['subcontext'][category]
    sortitems = [ int(n) for n in framework.keys() ]
    count = 0
    for item in sorted(sortitems):
        count += 1
        item = str(item)
        msg = '\t\t{:>2}'.format(item)
        sys.stdout.write(colors.color['white'] + msg)
        sys.stdout.write(colors.color['cyan'] + ' -  ')
        sys.stdout.write(colors.color['grey'] + '{0}\n'.format(framework[item]))
        sys.stdout.flush()

    back = '\n\t\t{0}\n'.format('Press "B" and ENTER to go back')
    sys.stdout.write(back)
    sys.stdout.flush()

    msg = colors.color['white'] + '\n\t\t{0} >  '.format('Select Incident Context')
    input = raw_input(msg)
    valid = validate_choice(framework, input, count)

    if valid == 'B'.lower():
        return 'B'.lower()

    if isinstance(valid, tuple):
        return valid

    else:
        retry = show_incident_subcontext(choice)
        return retry
#   ---


#   ---     INCIDENT ATTRIBUTES MENU    ---
def show_incident_severity():
    sys.stdout.write('\n\t\t               ')
    sys.stdout.write(colors.color['cyan'] + '[ ')
    sys.stdout.write(colors.color['white'] + 'INCIDENT SEVERITY TYPE')
    sys.stdout.write(colors.color['cyan'] + ' ]')
    sys.stdout.write('               \n\n')
    sys.stdout.flush()

    framework = settings['severity']
    count = 0
    for n in sorted(framework.keys()):
        count += 1
        sys.stdout.write(colors.color['white'] + '\t\t{0}'.format(n))
        sys.stdout.write(colors.color['cyan'] + ' -  ')
        sys.stdout.write(colors.color['grey'] + framework[n].upper() + '\n')

    back = '\n\t\t{0}\n'.format('Press "B" and ENTER to go back')
    sys.stdout.write(back)
    sys.stdout.flush()

    msg = colors.color['white'] + '\n\t\t{0} >  '.format('Select Severity Type')
    choice = raw_input(msg)
    valid = validate_choice(framework, choice, count)

    if valid == 'B'.lower():
        return 'B'.lower()

    if isinstance(valid, tuple):
        return valid

    else:
        retry = show_incident_severity()
        return retry


def show_incident_zones():
    sys.stdout.write('\n\t\t               ')
    sys.stdout.write(colors.color['cyan'] + '[ ')
    sys.stdout.write(colors.color['white'] + 'AFFECTED INCIDENT ZONE')
    sys.stdout.write(colors.color['cyan'] + ' ]')
    sys.stdout.write('               \n\n')
    sys.stdout.flush()

    framework = settings['zones']
    count = 0

    for n in sorted(framework.keys()):
        count += 1
        sys.stdout.write(colors.color['white'] + '\t\t{0}'.format(n))
        sys.stdout.write(colors.color['cyan'] + ' -  ')
        sys.stdout.write(colors.color['grey'] + framework[n].upper() + '\n')

    back = '\n\t\t{0}\n'.format('Press "B" and ENTER to go back')
    sys.stdout.write(back)

    msg = colors.color['white'] + '\n\t\t{0} >  '.format('Select Affected Zone')
    choice = raw_input(msg)
    valid = validate_choice(framework, choice, count)

    if valid == 'B'.lower():
        return 'B'.lower()

    if isinstance(valid, tuple):
        return valid

    else:
        retry = show_incident_zones()
        return retry


def show_incident_tiers():
    sys.stdout.write('\n\t\t               ')
    sys.stdout.write(colors.color['cyan'] + '[ ')
    sys.stdout.write(colors.color['white'] + 'AFFECTED TIER')
    sys.stdout.write(colors.color['cyan'] + ' ]')
    sys.stdout.write('               \n\n')
    sys.stdout.flush()
    framework = settings['tiers']
    count = 0
    for n in sorted(framework.keys()):
        count += 1
        for k,v in framework[n].iteritems():
            sys.stdout.write(colors.color['white'] + '\t\t{0}'.format(n))
            sys.stdout.write(colors.color['cyan'] + ' -')
            sys.stdout.write(colors.color['grey'] + '  {0}  {1}\n'.format(k.upper(), v))

    back = '\n\t\t{0}\n'.format('Press "B" and ENTER to go back')
    sys.stdout.write(back)

    msg = colors.color['white'] + '\n\t\t{0}'.format('Select Affected Tier >  ')
    choice = raw_input(msg)
    valid = validate_choice(framework, choice, count)


    if valid == 'B'.lower():
        return 'B'.lower()

    if isinstance(valid, tuple):
        return valid

    else:
        retry = show_incident_tiers()
        return retry


def show_incident_business_unit():
    sys.stdout.write('\n\t\t               ')
    sys.stdout.write(colors.color['cyan'] + '[ ')
    sys.stdout.write(colors.color['white'] + 'AFFECTED BUSINESS UNIT')
    sys.stdout.write(colors.color['cyan'] + ' ]')
    sys.stdout.write('               \n\n')
    sys.stdout.flush()

    framework = settings['business_orgs']
    count = 0

    for n in sorted(framework.keys()):
        count += 1
        sys.stdout.write(colors.color['white'] + '\t\t{0}'.format(n))
        sys.stdout.write(colors.color['cyan'] + ' -  ')
        sys.stdout.write(colors.color['grey'] + framework[n].upper() + '\n')

    back = '\n\t\t{0}\n'.format('Press "B" and ENTER to go back')
    sys.stdout.write(back)
    sys.stdout.flush()

    msg = colors.color['white'] + '\n\t\t{0} >  '.format('Select Affected Business Unit')
    choice = raw_input(msg)
    valid = validate_choice(framework, choice, count)

    if valid == 'B'.lower():
        return 'B'.lower()

    if isinstance(valid, tuple):
        return valid

    else:
        retry = show_incident_business_unit()
        return retry


#   --- Execute and Present Menu    ---
def animate():
    value = ''

    run = {}
    run[1] = show_incident_types
    run[2] = show_incident_subcontext
    run[3] = show_incident_severity
    run[4] = show_incident_zones
    run[5] = show_incident_tiers
    run[6] = show_incident_business_unit

    res = {}
    res[1] = ''
    res[2] = ''
    res[3] = ''
    res[4] = ''
    res[5] = ''
    res[6] = ''

    not_done = True
    step = 1
    tracker = 0
    while not_done:
        clear()
        if step == 2:
            value = run[step](res[1])
        else:
            value = run[step]()

        if isinstance(value, tuple):
            res[step] = value
            step += 1
            tracker += 1
            if tracker == 6:
                not_done = False

        elif isinstance(value, str):
            if value == 'B'.lower():
                res[step] = ''
                back = step - 1
                step -= 1
                tracker -= 1

            elif value == 'Q'.lower():
                not_done = False
    return res

if __name__ == '__main__':
    animate()
