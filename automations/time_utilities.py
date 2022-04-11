import time
from datetime import datetime   
import pytz

import environment

def convert_local_time_hm_to_UTC(localtime):
	local = pytz.timezone(environment.time_zone)
	naive = datetime.strptime(localtime, "%H:%M %p")
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

def get_UTC():
	return datetime.now(timezone.utc)

# utc_dt.strftime("%Y-%m-%d %H:%M:%S")
