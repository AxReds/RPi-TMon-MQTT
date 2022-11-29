#!/usr/bin/env python3
#to make the script executable added the above line (a shebang: a # + a !)
#read the readme file for details

#Raspberry-Pi Temperature Monitoring which publishes data to MQTT-Brocker (RPi-TMon-MQTT) - v1.0.
#Copyright (C) 2020 Alessio Rossini <alessior@live.com>
#Original source code available at https://github.com/AxReds/RPi-TMon-MQTT

#
#This program is free software; you can redistribute it and/or modify it under
#the terms of the GNU General Public License as published by the Free Software Foundation;
#either version 3 of the License, or any later version.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#See the GNU General Public License for more details
#https://opensource.org/
#
#You should have received a copy of the GNU General Public License along with this program; 
#if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
#
#

# import
import time
import paho.mqtt.client as mqtt #Import Paho MQTT Library
import json #Import json library
import os, sys
#include gpiozero library function to simplify the code
from gpiozero import CPUTemperature


#
#Define a function that returns current CPU temperature in float
def CPUTempF():
    #Read the temperature from Raspberry PI internal sensor
    cpuTemp = CPUTemperature()
    return(float(cpuTemp.temperature))
#
# MQTT on connect function
def on_connect(client, userdata, flags, rc) :
    print("Client che invia messaggi connesso con codice: " + str(rc))


#initialize json config file object
try:
    config_json = open('./config.json', 'r')
except:
    print ('Configuration file not found.\n')
    answ = input ('Please type "yes" to create a default file:')
    if  answ.lower() == 'yes' or answ.lower() == 'y':
        print ('File created!')
else:
    try:
        #read data from file 
        dati = json.load(config_json)
    except:
        print ('Invalid data in JSON config file.\n')
    else:
        #initialiaze variables
        username = dati['username']
        password = dati['password']
        Broker = dati["server"] # sets broker IP address
        port = dati["port"]
        time_out = dati["timeout"]
        topic = dati["topic"] #sets MQTT Topic


# instantiate paho MQTT client
client = mqtt.Client()

#set username and password
client.username_pw_set(username, password)

# add on_connect function to on_connect event
client.on_connect = on_connect

# connect paho client to mosquitto broker (IP, port, timeout)
client.connect(Broker, port, time_out)

# put client's loop in background
client.loop_start()

# send messages every 2 seconds
while True:
    #
    #Read the current temperature
    temp = CPUTempF()
    client.publish(topic, temp)
    time.sleep(2)


