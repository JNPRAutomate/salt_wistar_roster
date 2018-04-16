# salt_wistar_roster
A Salt roster module for Wistar


This repository contains a custom roster module for Salt that allows targetting hosts in a Wistar topology. Using this module, you can quickly spin up a topology in Wistar and target all the hosts automatically using salt-ssh.

### Installing this roster module

Copy the wistar.py roster module into the `_rosters` directory in your salt root directory

```bash
root@lab-01:~# ls -al /srv/salt/_roster/
total 12
drwxr-xr-x 2 root root 4096 Apr 16 18:41 .
drwxr-xr-x 9 root root 4096 Mar 20 17:15 ..
-rw-r--r-- 1 root root 2555 Apr 16 18:41 wistar.py
```

Sync this module using the saltutil.syncrosters runner

```bash
root@lab-01:/srv/salt/_roster# salt-run saltutil.sync_roster
- roster.wistar
```

### Specify a topology to target

Copy the URL from the topologies/edit.html screen in Wistar for a deployed topology. 

```bash
export WISTAR_URL='http://10.10.10.0:8085/topologies/2/'
```

### Using this roster module


```bash
root@lab-01:~# salt-ssh --roster wistar 'svl-edi*'  cmd.run 'uptime'
svl-edi-01:
     20:45:09 up 4 days, 22:28,  0 users,  load average: 0.00, 0.02, 0.00
svl-edi-02:
     20:45:09 up 4 days, 22:27,  0 users,  load average: 0.10, 0.10, 0.09

```

You can use any available Salt module via salt-ssh to configure the various hosts in your topology. 


### Example workflow

1. Create a new topology in Wistar
2. Deploy and launch the desired hosts in this topology
3. Copy the URL into the WISTAR_URL and export it on the salt-master
4. Use salt-ssh with the wistar module to target the hosts to install python

```bash
salt-ssh --roster wistar test-instance-01 -r 'apt-get install python -y'
salt-ssh --roster wistar test-instance-01 state.apply linux.dns_server
salt-ssh --roster wistar test-instance-01 cmd.run 'uptime'
```
