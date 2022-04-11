import environment as env
import requests
import json

from urllib3.util import connection
from urllib3.util import ssl_match_hostname

_orig_create_connection = connection.create_connection

def custom_resolver(host):
	print(host)
	if host == 'ecb5fafffe9bddec':
		return '192.168.0.44'
	else:
		return host


def patched_create_connection(address, *args, **kwargs):
    """Wrap urllib3's create_connection to resolve the name elsewhere"""
    # resolve hostname to an ip address; use your own
    # resolver here, as otherwise the system resolver will be used.
    host, port = address
    hostname = custom_resolver(host)

    return _orig_create_connection((hostname, port), *args, **kwargs)


connection.create_connection = patched_create_connection


headers = {'hue-application-key' : env.hue_application_key}
verify = False


def get(url):
	return requests.get(url=url, headers=headers, verify=verify)

def put(url, json):
	return requests.put(url=url, headers=headers, json=json, verify=verify) 		
