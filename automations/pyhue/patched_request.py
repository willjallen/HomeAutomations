import environment as env
import requests
import json

from urllib3.util import connection
from urllib3.util import ssl_match_hostname

from utils.bridge_utils import BRIDGE_IP

import warnings

_orig_create_connection = connection.create_connection

# TODO the ip will change over time and break this
# implement this https://discovery.meethue.com/	
def custom_resolver(host):
	if host == env.hue_bridge_id:
		if(BRIDGE_IP != -1):
			return BRIDGE_IP
		else:
			raise ValueError('Hue Bridge IP not found')
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
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		return requests.get(url=url, headers=headers, verify=verify)

def put(url, json):
	with warnings.catch_warnings():
		warnings.simplefilter('ignore')
		return requests.put(url=url, headers=headers, json=json, verify=verify) 		

