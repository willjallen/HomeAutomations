import os
from dotenv import load_dotenv

load_dotenv()
hue_application_key = os.getenv("HUE-APPLICATION-KEY")
url = os.getenv("URL")
cert = os.getenv("CERT")