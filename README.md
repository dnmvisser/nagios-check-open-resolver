# nagios-check-open-resolver

### Summary

Nagios plugin to check for an open DNS resolver


### Usage

```
usage: check-open-resolver.py [-h] -H HOST [-d DOMAIN] [--type TYPE]
                              [--timeout TIMEOUT] [-v]

Nagios plugin to test if an open resolver exists

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Hostname to test
  -d DOMAIN, --domain DOMAIN
                        DNS domain to query
  --type TYPE           DNS query type
  --timeout TIMEOUT     Timeout when doing DNS query
  -v, --verbosity       Increase output verbosity
```

### Examples

```
debian@foo:~$ ./check-open-resolver.py -H 192.168.0.1
OK: No resolver found on 192.168.0.1
```


```
# DNS0 resolver
debian@foo:~$ ./check-open-resolver.py -H 2a0f:fc80::
CRITICAL: Host 2a0f:fc80:: resolves DNS queries
```
