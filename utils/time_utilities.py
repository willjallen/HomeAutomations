import time
from datetime import datetime   
import pytz

import environment as env

def convert_local_time_hm_to_UTC(localtime):
	local = pytz.timezone(env.time_zone)
	naive = datetime.strptime(localtime, "%Y-%m-%d %H:%M %p")
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

def get_local_time():
	return datetime.now(pytz.timezone(env.time_zone))

def get_UTC():
	return datetime.now(pytz.utc)

# utc_dt.strftime("%Y-%m-%d %H:%M:%S")
