from datetime import datetime, time, timedelta 
import pytz

import environment as env

local_timezone = pytz.timezone(env.time_zone) 
utc_timezone = pytz.utc

def convert_local_time_hm_to_UTC(localtime):
	naive = datetime.strptime(localtime, "%Y-%m-%d %I:%M %p")
	local_dt = local_timezone.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

def get_local_time():
	return datetime.now(local_timezone)

def get_UTC_time():
	return datetime.now(utc_timezone)

# def get_before_midnight_today_UTC():
# 	tz = pytz.timezone(env.time_zone) # choose timezone

# 	# 1. get correct date for the midnight using given timezone.
# 	today = datetime.now(tz).date()

# 	# 2. get midnight in the correct timezone (taking into account DST)
# 	#NOTE: tzinfo=None and tz.localize()
# 	# assert that there is no dst transition at midnight (`is_dst=None`)
# 	midnight = tz.localize(datetime.combine(today, time(11, 59)), is_dst=None)

	# return midnight.astimezone(pytz.utc)

def get_local_tomorrow_start():
	dt_now = get_local_time()
	tomorrow_start = datetime(dt_now.year, dt_now.month, dt_now.day).astimezone(local_timezone) + timedelta(1)
	return tomorrow_start

def get_tomorrow_start_as_utc():
	local_tomorrow_start = get_local_tomorrow_start()
	utc_tomorrow_start = local_tomorrow_start.astimezone(pytz.utc)
	return utc_tomorrow_start

def UTC_timestamp_to_local_datetime(timestamp):
	tz = pytz.timezone(env.time_zone)
	return datetime.fromtimestamp(timestamp, tz)

# utc_dt.strftime("%Y-%m-%d %H:%M:%S")
