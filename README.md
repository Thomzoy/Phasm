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

## RaspAP settings

By default:

- IP is `10.3.141.1`, with root credentials being (`admin`,`secret`)
- SSID is `raspi-webgui`, with password being `ChangeMe`

## Dash Settings

The app should run on the host provided by RaspAP, on port 8000:

```
app.run_server(port=8000, host="10.3.141.1", debug=True)
```

## Next Steps

- Try with `Node-RED` ?
