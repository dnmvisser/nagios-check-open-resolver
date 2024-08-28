# nagios-check-open-resolver

### Summary

Nagios plugin to check for an open DNS resolver

### Usage

```
usage: check-open-resolver.py [-h] -H HOST [-d DOMAIN] [--type TYPE]
                              [--timeout TIMEOUT]

Nagios plugin to test if an open resolver exists at an IP address or hostname

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Hostname to test (default: None)
  -d DOMAIN, --domain DOMAIN
                        DNS domain for the test query (default: google.com)
  --type TYPE           DNS type for the test query (default: A)
  --timeout TIMEOUT     Timeout for the test query (default: 2)
```

### Examples

```
debian@foo:~$ ./check-open-resolver.py -H 192.168.0.1
OK: No resolver found on 192.168.0.1
```


```
# Google's open resolver - should resolve
debian@foo:~$ ./check-open-resolver.py -H dns.google.com
CRITICAL: dns.google.com resolves DNS queries
```
