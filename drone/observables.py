#coding: utf-8

__author__  = "@DFIRENCE | CARLOS DIAZ"
__version__ = "0.0.1"
__license__ = "MIT"

import multiprocessing as mp
from sys import stdout
from time import sleep

def upload_observables(hiveapi, caseid, hiveid, hivecase, observables, tag):
    '''
        Uploads data to the REST API Service of your instance of TheHive

        :param hiveapi:         An instance of TheHiveApi object configured with url & apikey
        :param caseid:          A numeric `number` record of a case created in TheHive
        :param hiveid:          An elasticsearch unique-id of a record created in TheHive
        :param hivecase:        A custom python dictionary aligned to REST API Spec for Observables
        :param observables:     A custom python list of values containing observables for uploads
        :param tag:             A custom flag set to extract observables and upload these to TheHive
    '''
    msg = "(+) Case {:7}{:>15}\t\t( {:>7}/{:<7} )  |  ( {:>7} )"
    total = len(observables)
    counter_success = 0
    counter_failure = 0
    items = []
    for item in observables:
        hivecase.load_observable(item, tag, caseid)
        items.append(hivecase.observable)

    for data in items:
        try:
            http = hiveapi.create_observable(hiveid, data)
            if http.status_code == 201:
                counter_success += 1
                stdout.write("\r" + msg.format(caseid, tag.upper(), total, counter_success, counter_failure))
                stdout.flush()
            else:
                counter_failure += 1
        except Exception as http_observable_upload:
            counter_failure += 1
            print http_observable_upload
    stdout.write("\n")
    stdout.flush()

def process_observables(hiveapi, caseid, hiveid, case, hivecase, datatags):
    '''
        A multiprocess approach to uploading observables based on `tag` type
        :param hiveapi:         An instance of TheHiveApi object configured with url & apikey
        :param caseid:          A numeric `number` record of a case created in TheHive
        :param hiveid:          An elasticsearch unique-id of a record created in TheHive
        :param case:            A custom python dictionary aligned to REST API  Spec for Cases
        :param hivecase:        A custom python dictionary aligned to REST API Spec for Observables
        :param datatags:        A custom set of flags to signal the type of observables to process
    '''

    headers = ("Data Type", "Uploaded", "Failed")
    msg     = "\n{:>33}\t\t{:>10}{:>15}\n{}\n".format(headers[0], headers[1], headers[2], "-" * 110)
    stdout.write(msg)
    stdout.flush()
    pids = []

    # Create a process pid object for each observable list
    for idx, tag in enumerate(datatags):
        observables = case.sin['observables'][tag]
        pid = mp.Process(target=upload_observables, args=(hiveapi, caseid, hiveid, hivecase, observables, tag,))
        pids.append(pid)

    linecount = "\n" * len(datatags)
    stdout.write(linecount)

    for job in pids:
        job.start()

    for job in pids:
        job.join()
