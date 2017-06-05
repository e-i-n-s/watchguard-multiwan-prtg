import urllib
import http.cookiejar
import ssl
import xml.etree.ElementTree as ET
import json
import argparse
from paepy.ChannelDefinition import CustomSensorResult

parser = argparse.ArgumentParser()
parser.add_argument("prtg", help="PRTG String")
args = parser.parse_args()
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
cookiejar = http.cookiejar.CookieJar()
cookiejar.clear_session_cookies()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar),urllib.request.HTTPSHandler(context=context))

parameters = json.loads(args.prtg);
host = parameters.get('host')
user = parameters.get('linuxloginusername') 
password = parameters.get('linuxloginpassword') 
baseURL = 'https://' + host + ':8080'

def etree_to_dict(t):
    return {t.tag : map(etree_to_dict, t.iterchildren()) or t.text}

url = baseURL + '/agent/login'
data = '<methodCall><methodName>login</methodName><params><param><value><struct><member><name>password</name><value><string>' + password +'</string></value></member><member><name>user</name><value><string>' + user + '</string></value></member><member><name>domain</name><value><string>Firebox-DB</string></value></member><member><name>uitype</name><value><string>2</string></value></member></struct></value></param></params></methodCall>'

req = urllib.request.Request(url, data.encode('utf-8'))
response = opener.open(req)
xmlUserInformation = response.read()

root = ET.fromstring(xmlUserInformation)
sid = root[0][0][0][0][0][1].text
csrfToken = root[0][0][0][0][1][1].text

url = baseURL + '/auth/login'
values = [('username', user),
          ('password', password),
          ('domain','Firebox-DB'),
          ('sid',sid),
          ('privilege',1),
          ('from_page','/')]

data = urllib.parse.urlencode(values)
req = urllib.request.Request(url=url,data=data.encode('utf-8'))
response = opener.open(req)


url = baseURL + '/dashboard/dboard_get_interfaces?id=undefined'
req = urllib.request.Request(url)
response = opener.open(req)

# Parse JSON
interfaces = json.loads(response.read().decode('utf8'));
xmlList = interfaces.get('interface_list');

# Parse XML
list = ET.fromstring(xmlList)
list_interfaces = list.find('network').find('interface_list')

count_external_interfaces = 0
failed_interfaces = []
for interface in list_interfaces.getchildren():
    if interface.find('enabled').text == '1' and interface.find('zone').text == 'External':
        count_external_interfaces += 1
        if interface.find('wan_target_status').text == '0':
            failed_interfaces.append(interface.find('ifalias').text)

message = 'WAN Status: Error';
status = 2
if len(failed_interfaces) is 0:
    message = 'OK'
    status = 0

sensor = CustomSensorResult(message) 
sensor.add_channel(channel_name="Status",unit="Count",value=status,is_limit_mode=True,limit_max_error=0,limit_error_msg="At least one WAN is not available!", primary_channel=True)
sensor.add_channel(channel_name="Failed",unit="Count",value=len(failed_interfaces),is_limit_mode=True,limit_max_error=0)
print(sensor.get_json_result())