# RPi-TMon-MQTT

Raspberry-Pi Temperature Monitoring with MQTT integration (RPi-TMon-MQTT)
Copyright (C) 2022 Alessio Rossini alessior@live.com

This is a Python script for reading the currente CPU temperature of a Raspberry PI device and publishing the data to an MQTT broker. The script also has some logic for handling errors and retrying failed MQTT connections.

## Libraries
The code requires the following libraries:

- `gpiozero`
- `paho.mqtt.client`

## Constants
The script defines some constants for the MQTT connection parameters (e.g. broker address, client ID).
Constants are initialized reading the configuration file `config.json`

## Infinite Loop
The script sets up an infinite loop to periodically read the temperature data from the internal sensor of the RPi and publish it to the MQTT broker. 
The data can then be consumed from the MQTT by any MQTT Client

