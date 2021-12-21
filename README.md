# Phasm

## RPi installation

- Install `usbmuxd` (Internet connection via USB)

- Install `virtualenv` 

- Install `RaspAP` (Wi-Fi Access Point)
   - Change the WiFi region in the Pi settings beforehands !
   - During the RaspAP install, do not add the ad-blocker or the VPN

- Install `mosquitto` (MQTT Broker)

- Install `streamlit` **version 0.62**
   - ⚠️ version 0.63 and above depends on `pyarrow` which currently doesn't work well on the Pi3 (at least on the 32 bits version)


## Mosquitto settings

Configuration is done via a `mosquitto.conf` file.
The minimal configuration should tell Mosquitto to use the IP provided by RaspAP, which is `10.3.141.1` by default. Default port for MQTT is `1883`.
So add this lise to the `mosquitto.conf` file:

```
listener 1883 10.3.141.1
```

Then launch the service via `mosquitto -c ./mosquitto.conf`
