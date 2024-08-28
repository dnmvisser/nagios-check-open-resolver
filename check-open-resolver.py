#!/usr/bin/env python3
import argparse
import sys
import dns.resolver

parser = argparse.ArgumentParser(
    description="Nagios plugin to test if an open resolver exists"
)
parser.add_argument("-H", "--host", help="Hostname to test", required=True)
parser.add_argument("-d", "--domain", help="DNS domain to query", default="google.com")
parser.add_argument("--type", help="DNS query type", default="A")
parser.add_argument("--timeout", help="Timeout when doing DNS query", default=2)
parser.add_argument(
    "-v", "--verbosity", action="count", default=0, help="Increase output verbosity"
)

args = parser.parse_args()

host = args.host
domain = args.domain
query_type = args.type
timeout = float(args.timeout)
verbosity = args.verbosity


# Functions
def nagios_exit(message, code):
    print(message)
    sys.exit(code)


# Possible nagios statuses
# See https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html
msg = {"ok": [], "warning": [], "critical": [], "unknown": []}

res = dns.resolver.Resolver()
res.nameservers = [host]
res.timeout = timeout
res.lifetime = timeout


try:
    is_resolver = bool(res.resolve(domain))
except Exception:
    is_resolver = False

if is_resolver:
    msg["critical"].append(f"Host {host} resolves DNS queries")
else:
    msg["ok"].append(f"No resolver found on {host}")

# Exit with accumulated message(s)
if len(msg["critical"]) > 0:
    nagios_exit("CRITICAL: " + " ".join(msg["critical"]), 2)
elif len(msg["warning"]) > 0:
    nagios_exit("WARNING: " + " ".join(msg["warning"]), 1)
else:
    nagios_exit("OK: " + " ".join(msg["ok"]), 0)
