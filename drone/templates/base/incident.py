#coding: utf-8
from os import path
from datetime import datetime

import iptools
import jinja2 as J

def render(cirt):
    file = __file__
    abspath = path.dirname(path.abspath(file))
    abspath = abspath.replace('\\base','')
    abspath = path.join(abspath, 'jinja')
    template = path.join(abspath, 'incident_plain_html.jinja')
    
    with open(template, 'rb') as html:
        content = ''.join(html.readlines())
	
	t = J.Template(content)
	t = t.render(
        sin      = cirt.sin['restapi']['caseId'],
		cat 	 = cirt.sin['tags'][1]		,
		type 	 = cirt.sin['tags'][6] + " - " + cirt.sin['tags'][7],
		severity = cirt.sin['tags'][2]      ,
		zone	 = cirt.sin['tags'][3]		,
		tier	 = cirt.sin['tags'][4]		,
		agency	 = cirt.sin['tags'][5]		,
		time	 = datetime.now()			,
		overview = cirt.sin['description']  ,
		
        URL_VALUES              = cirt.sin['observables']['urls']	    ,
		DOMAIN_VALUES 	        = cirt.sin['observables']['fqdns']	    ,
		USER_VALUES		        = cirt.sin['observables']['ldap_user']	,
		#HOSTNAME_VALUES        = cirt.sin['observables']['ldap_host']	,
		SRC_IP_VALUES	        = cirt.sin['observables']['src_ip']	    ,
		DST_IP_VALUES	        = cirt.sin['observables']['dst_ip']     ,
		HASH_VALUES             = cirt.sin['observables']['hashes']     ,
        EMAIL_SENDER_VALUES     = cirt.sin['observables']['src_email']  ,
        EMAIL_RECIPIENT_VALUES  = cirt.sin['observables']['dst_email']  ,
        PRIVATE_IPS_RFC1918     = iptools.IpRangeList(
                                        '127.0.0.1'     ,
                                        '10.0.0.1/8'    ,
                                        '172.16.0.1/20' ,
                                        '192.168.0.1/16'
                                ),
        PRIVATE_ORG_DOMAINS = (
            'hqad.mtahq.org'    ,
            'mtahq.org'         ,
            'mtabt.org'         ,
            'nyct.com'          ,
            'lirr.org'          ,
            'mnr.org'           ,
            'mtabsc.org'        ,
            'transit.nyct.com'  ,
            'lirrad.lirr.org'   ,
            'pdad.mta-pd.org'
        )
    )
	cirt.sin['template'] = t
	return cirt



def test():
    file = __file__
    abspath = path.dirname(path.abspath(file))
    print abspath.replace('\\base','')
    repl = abspath.replace('\\base','')
    abspath = path.join(repl, 'jinja')
    template = path.join(abspath, 'incident_plain_html.jinja')
    print repl
    print abspath
    print template
    if path.exists(template):
        print '[+] FOUND TEAMPLE'
    else:
        print '[-] NOT FOUND'
    
if __name__ == '__main__':
    test()