#!/usr/bin/env python3
import argparse
import sys
import netaddr
import dns.resolver

parser = argparse.ArgumentParser(
    description="Nagios plugin to test if an open resolver exists at an IP address or hostname",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("-H", "--host", help="Hostname to test", required=True)
parser.add_argument(
    "-d", "--domain", help="DNS domain for the test query", default="google.com"
)
parser.add_argument("--type", help="DNS type for the test query", default="A")
parser.add_argument("--timeout", help="Timeout for the test query", default=2)
args = parser.parse_args()

host = args.host
domain = args.domain
query_type = args.type
timeout = float(args.timeout)


# Functions
def nagios_exit(message, code):
    print(message)
    sys.exit(code)


# Possible nagios statuses
# See https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/pluginapi.html
msg = {"ok": [], "warning": [], "critical": [], "unknown": []}

res = dns.resolver.Resolver()
res.timeout = timeout
res.lifetime = timeout


def is_resolver(addr):
    res.nameservers = [addr]
    try:
        return bool(res.resolve(domain))
    except Exception:
        return False


def is_addr(string):
    try:
        return netaddr.IPAddress(string)
    except Exception:
        return False


def resolve(hostname, t):
    try:
        # TODO iterate over all addresses
        return res.resolve(hostname, t)[0].to_text()
    except Exception:
        return False


# Start
found_resolvers = []

if is_addr(host):
    if is_resolver(host):
        found_resolvers.append(host)
else:
    v4 = resolve(host, "A")
    v6 = resolve(host, "AAAA")
    if v4:
        if is_resolver(v4):
            found_resolvers.append(v4)
    if v6:
        if is_resolver(v6):
            found_resolvers.append(v6)
    if not v4 and not v6:
        msg["unknown"].append(f"Unable to resolve hostname {host}")

if len(found_resolvers) > 0:
    msg["critical"].append(f"{host} resolves DNS queries")
else:
    msg["ok"].append(f"No resolver found on {host}")

# Exit with accumulated message(s)
if len(msg["unknown"]) > 0:
    nagios_exit("UNKNOWN: " + " ".join(msg["unknown"]), 3)
elif len(msg["critical"]) > 0:
    nagios_exit("CRITICAL: " + " ".join(msg["critical"]), 2)
elif len(msg["warning"]) > 0:
    nagios_exit("WARNING: " + " ".join(msg["warning"]), 1)
else:
    nagios_exit("OK: " + " ".join(msg["ok"]), 0)
