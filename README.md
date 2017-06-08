# Watchguard MultiWAN with PRTG

## Requirements
- WatchGuard (tested with Firmware >= 11.12.0, non-cluster or cluster) 
- A 'Device Monitor' User (you can use the status user or add a new user)
- PRTG (tested with version 17)

## Setup
- Add script to 'C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python' (PRTG Probe Server)
- Add 'Device Monitor' user credentials to the Firewall device as Linux credentials
- IN PRTG Web UI: Add new sensor 'Python Script (Advanced)' and select the script you copied

## Test the script from a command line
`python watchguard-multiWAN.py "{\"host\":\"%HOST%\",\"linuxloginusername\":\"%USER%\",\"linuxloginpassword\":\"%PASSWORD%\"}"`


