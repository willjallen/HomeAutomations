from datetime import datetime, time 
import pytz

import environment as env

def convert_local_time_hm_to_UTC(localtime):
	local = pytz.timezone(env.time_zone)
	naive = datetime.strptime(localtime, "%Y-%m-%d %I:%M %p")
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

def get_local_time():
	return datetime.now(pytz.timezone(env.time_zone))

def get_UTC():
	return datetime.now(pytz.utc)

def get_midnight_today_UTC():
	tz = pytz.timezone(env.time_zone) # choose timezone

	# 1. get correct date for the midnight using given timezone.
	today = datetime.now(tz).date()

	# 2. get midnight in the correct timezone (taking into account DST)
	#NOTE: tzinfo=None and tz.localize()
	# assert that there is no dst transition at midnight (`is_dst=None`)
	midnight = tz.localize(datetime.combine(today, time(11, 59)), is_dst=None)

	return midnight.astimezone(pytz.utc)

def UTC_timestamp_to_local_datetime(timestamp):
	tz = pytz.timezone(env.time_zone)
	return datetime.fromtimestamp(timestamp, tz)

# utc_dt.strftime("%Y-%m-%d %H:%M:%S")
