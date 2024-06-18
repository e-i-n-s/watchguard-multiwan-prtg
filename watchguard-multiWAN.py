import urllib
import http.cookiejar
import sys
import ssl
import xml.etree.ElementTree as ET
import json
import argparse
from paesslerag_prtg_sensor_api.sensor.result import CustomSensorResult
from urllib.parse import quote

# Prepare data and web session
data = json.loads(sys.argv[1])
parser = argparse.ArgumentParser()
parser.add_argument("prtg", help="PRTG String")
args = parser.parse_args()
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
cookiejar = http.cookiejar.CookieJar()
cookiejar.clear_session_cookies()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar),
                                     urllib.request.HTTPSHandler(context=context))
# Firewall connection
parameters = json.loads(args.prtg)
host = parameters.get('host')
user = parameters.get('linuxloginusername')
password = parameters.get('linuxloginpassword')
encode_password = quote(password)
baseURL = 'https://' + host + ':8080'

url = baseURL + '/auth/login/' + user + '/' + encode_password
req = urllib.request.Request(url)
response = opener.open(req)

url = baseURL + '/dashboard/dboard_get_interfaces?id=undefined'
req = urllib.request.Request(url)
response = opener.open(req)

# JSON Response
interfaces = json.loads(response.read().decode('utf8'))
xmlList = interfaces.get('interface_list')

# XML
list = ET.fromstring(xmlList)
if list[0].tag == 'cluster':
    list = list.find('cluster').find('aggregate')
list_interfaces = list.find('network').find('interface_list')

count_external_interfaces = 0
failed_interfaces = []

# Browse interfaces to check their status
for interface in list_interfaces:
    if interface.find('enabled').text == '1' and interface.find('zone').text == 'External':
        count_external_interfaces += 1
        if interface.find('wan_target_status').text == '0':
            failed_interfaces.append(interface.find('ifalias').text)

# Concatenate interface names
failed_interfaces_str = ', '.join(failed_interfaces) if failed_interfaces else 'Aucune'

# Adjusting messages and status
if len(failed_interfaces) == 0:
	message = 'OK'
else:
	message = 'Failed WAN : ' + failed_interfaces_str

# Sensor creation
csr = CustomSensorResult(text=message)
csr.add_primary_channel(name="Status",
						unit="WAN Failed",
						value=len(failed_interfaces),
						is_limit_mode=True,
						limit_max_error=0.5)

# Print result in JSON format for PRTG
print(csr.json_result)
