# Watchguard MultiWAN with PRTG

**No support for SD-WAN**


## Requirements
- WatchGuard (tested with Firmware 12.10.2, non-cluster or cluster) 
- A 'Device Monitor' User (you can use the status user or add a new user)
- PRTG (tested with version 24.1.92)

## Setup
- Add script to 'C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python' (PRTG Probe Server)
- Add 'Device Monitor' user credentials to the Firewall device as Linux credentials
- IN PRTG Web UI: Add new sensor 'Python Script (Advanced)' and select the script you copied

## Testing
**You cannot test this script in Windows because it uses the "paesslerag_prtg_sensor_api" class specific to PRTG's python system.**


