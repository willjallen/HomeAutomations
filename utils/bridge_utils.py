import subprocess 
import environment as env

BRIDGE_IP = 0


def get_bridge_ip():

	command = ['nmap', '-sn', '192.168.1.1-254']

	out = subprocess.run(command, capture_output=True)
	outstr = out.stdout.decode('utf-8')

	# nmap scan has MAD address in EUI-48 format, hostname is EUI-64
	# to convert EUI-64 -> EUI-48 there is an fffe added in the middle, 6 chars in
	id_loc = outstr.find(env.hue_bridge_id[0:6] + env.hue_bridge_id[10:16])
	if(id_loc != -1):
		# Nmap scan report for xxxxxxxxxxxx (192.168.1.31)
		# 									^            ^
		return outstr[id_loc + 14 : id_loc + 26]
	else:
		return -1

# TODO: this is so dumb. Fix this.
BRIDGE_IP = '192.168.1.31' 
print(BRIDGE_IP)
