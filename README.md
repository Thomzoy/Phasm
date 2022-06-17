# Phasm

## RPi installation

- Install `usbmuxd` (Internet connection via USB)

- Install `virtualenv` 

- Install `RaspAP` (Wi-Fi Access Point)
   - Change the WiFi region in the Pi settings beforehands !
   - During the RaspAP install, do not add the ad-blocker or the VPN

- Install `mosquitto` (MQTT Broker)

- Install the required packages via 
```
cd dash
pip install -r requirements.txt
```

- **DEPRECIATED** Install `streamlit` **version 0.62**
   - ⚠️ version 0.63 and above depends on `pyarrow` which currently doesn't work well on the Pi3 (at least on the 32 bits version)


## Mosquitto settings

Configuration is done via the `/etc/mosquitto/mosquitto.conf` file.
The minimal configuration should tell Mosquitto to use the IP provided by RaspAP, which is `10.3.141.1` by default. Default port for MQTT is `1883`.
For the moment we want everybody to be able to interact with the brocker
So add these lines to the `mosquitto.conf` file:

```
listener 1883 10.3.141.1

allow_anonymous true
```

Then mosquitto should be handled as a service:
- Starting via `systemctl start mosquitto`
- Checking status via `systemctl status mosquitto`
- Stopping via `systemctl stop mosquitto`

The service should be able to start at boot.  
However, it has to be able to connect to the IP provided by RaspAP, which can take some time to be ready.  
To tackle this, increase the retry period of the Mosquitto service to e.g. 5 seconds (default is 100ms) to make some time.  
To do so, modify the file at `/lib/systemd/system/mosquitto.service`:

```
[Unit]
Description=Mosquitto MQTT Broker
Documentation=man:mosquitto.conf(5) man:mosquitto(8)

[Service]
Type=notify
NotifyAccess=main
ExecStart=/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
ExecReload=/bin/kill -HUP $MAINPID
# Restart necessary to handle the time needed by RaspAP to make the adress available
Restart=on-failure
RestartSec=5
ExecStartPre=/bin/mkdir -m 740 -p /var/log/mosquitto
ExecStartPre=/bin/chown mosquitto /var/log/mosquitto
ExecStartPre=/bin/mkdir -m 740 -p /run/mosquitto
ExecStartPre=/bin/chown mosquitto /run/mosquitto
ExecStartPre=/bin/mkdir -m 740 -p /var/run/mosquitto
ExecStartPre=/bin/chown mosquitto /var/run/mosquitto

[Install]
WantedBy=multi-user.target
```

**Some notes**

- Check the list of services via `systemctl list-units --type=service`
- Following [this post](https://github.com/eclipse/mosquitto/issues/1950) might be useful

## RaspAP settings

By default:

- IP is `10.3.141.1`, with root credentials being (`admin`,`secret`)
- SSID is `raspi-webgui`, with password being `ChangeMe`

**Current setting**: SSID is `Phasm`, password is `HarryThePhasm`

The RaspAP service should be set up to launch **before** Mosquitto, since the later needs the IP address provided by RaspAP.  

To do so, change the config file of the RaspAP daemon located at `/lib/systemd/system/raspapd.service`:

```
### BEGIN INIT INFO
# Provides:          raspapd
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     S 2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start RaspAP daemon at boot time
# Description:       Enable service provided by daemon
### END INIT INFO
# Author: BillZ <billzimmerman@gmail.com>

[Unit]
Description=RaspAP Service Daemon
DefaultDependencies=no
Before=mosquitto.service

[Service]
Type=oneshot
ExecStart=/bin/bash /etc/raspap/hostapd/servicestart.sh --interface uap0 --seconds 3

[Install]
WantedBy=multi-user.target
```

Then reload the service via `sudo systemctl daemon-reload`

## Using a USB antenna

The one used currently is *Realtek Semiconductor Corp. RTL88x2bu [AC1200 Techkey]*.  

An installation guide for the driver can be found [here](https://github.com/morrownr/88x2bu-20210702)

**For it to work with RaspAP**:

1. Install the driver
2. Open the RaspAP admin page and change all mentions of `wlan0` (internal WiFi) to `wlan1` (external WiFi)
3. At this point, it might be buggy: restart the Pi.
4. The GUI might not be available atthis point. We have to manually change some settings:
    **a.** Edit `/var/www/html/includes/config.php` by setting `RASPI_WIFI_AP_INTERFACE` to `wlan1`  
    **b.** In this file, paths to other config files are mentionned, where changing from `wlan0` to `wlan1` is needed, namely:  
    **c.** `/etc/hostapd/hostapd.conf`  
    **d.** `/etc/dhcpcd.conf`  


## Dash Settings

The app should run on the host provided by RaspAP, on port 8000:

```
app.run_server(port=8000, host="10.3.141.1", debug=True)
```

## Next Steps

- Try with `Node-RED` ?



## Conda setup
```bash
conda create -n sceno
conda activate sceno
conda install pip
pip install RPi.GPIO dash-bootstrap-components tinydb dash-daq paho-mqtt gpiozero
```
