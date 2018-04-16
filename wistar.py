# Simple Salt dynamic roster module to pull all hosts from a wistar topology
# to use first set some ENV variables like
# bash: export WISTAR_URL='http://10.10.10.10:8080/topologies/27/'
# make sure this file is in /srv/salt/_roster
# sync rosters with salt-run saltutil.sync_roster
# then run with
# salt-ssh --roster wistar \*  test.ping
#
# nembery 2018-04-05
#
# Lots of work still to do!

import requests
import fnmatch
import re


def targets(tgt, tgt_type='glob', **kwargs):
    d = __runner__['salt.cmd'](fun="environ.items")

    if 'WISTAR_URL' not in d:
        print 'Error: No Wistar URL found in the environment. Please set to something like ' \
              '`export WISTAR_URL=http://10.10.10.1/topologies/24'
        return dict()

    print d['WISTAR_URL']

    m = re.search('(http.*)/topologies/(\d+)', d['WISTAR_URL'])

    if m and len(m.groups()) == 2:
        wistar_host = m.groups()[0]
        wistar_topology = m.groups()[1]

        wistar_export = wistar_host + '/topologies/export/' + wistar_topology

        r = requests.get(wistar_export)

        if r.status_code == 200:
            tj = r.json()
            all_hosts = __get_inv(tj)
            if tgt_type == 'glob':
                return ret_glob_minions(all_hosts, tgt)
            else:
                return dict()
        else:
            print 'Error: Could not contact wistar at: %s' % wistar_host

    # no wistar configuration found in env, just bail out here...
    print 'Error: Could not parse WISTAR_URL from %s' % d['WISTAR_URL']
    return dict()


def __get_inv(topology_json):
    hosts = dict()
    for json_object in topology_json:
        if "userData" in json_object and "wistarVm" in json_object["userData"]:
            ud = json_object["userData"]

            if "parentName" not in ud:
                # child VMs will have a parentName attribute
                # let's skip them for inventory automation purposes
                name = ud.get('name', 'no name')
                ip = ud.get('ip', '0.0.0.0')
                username = ud.get('username', 'root')
                password = ud.get('password', 'Clouds123')
                hosts[name] = dict()
                hosts[name]['host'] = ip
                hosts[name]['user'] = username
                hosts[name]['passwd'] = password

    return hosts


def ret_glob_minions(hosts, tgt):
    matched_minions = dict()
    for minion in hosts:
        if fnmatch.fnmatch(minion, tgt):
            matched_minions[minion] = hosts[minion]

    return matched_minions


