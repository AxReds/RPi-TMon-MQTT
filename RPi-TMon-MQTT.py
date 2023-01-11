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
import time, os, sys
import paho.mqtt.client as mqtt #Import Paho MQTT Library
import json #Import json library
if os.uname()[4] == 'aarch64': #verify if running on a Raspberry Pi 64bit architecture
    from gpiozero import CPUTemperature #include gpiozero library function to simplify the code


#
#Define a function that returns current CPU temperature in float
def CPUTempF():
    #Read the temperature from Raspberry PI internal sensor
    cpuTemp = CPUTemperature()
    return(float(cpuTemp.temperature))
#
# Define function on_connect for MQTT connection
def on_connect(client, userdata, flags, rc) :
    print("Process started and exited with code: " + str(rc))

#Initialize setup KO
set_up_ok=False
    
try:
    #verifies file exist
    config_json = open (os.path.join(os.path.dirname(__file__), 'config.json'), 'r') 
except:
    #file does not exist and then creates it
    print ('\n\nConfiguration file not found.')
    answ = input ('Please type "yes" or "y" to create a default file:')
    if  answ.lower() == 'yes' or answ.lower() == 'y' or answ.lower() =='':
        #defines json file structure
        dictionary = {'username':'your_username',
                      'password':'your__password',
                      'server':'your_mqqt_server_ip_or_fqdn',
                      'port':'your_server_tcp_port',
                      'timeout':'your_server_timeout',
                      'topic':'your_topic'}
        
        #creates a new file
        with open (os.path.join(os.path.dirname(__file__), 'config.json'), 'a') as f:
            #format the json data and write to file
            f.write (json.dumps (dictionary, indent=4))
        print ('File created!\nPlease, update the file ' + os.path.join(os.path.dirname(__file__), 'config.json') + ' and rerun the program.\n\n')
else:
    try:
        #read data from file 
        dati = json.load(config_json)
    except:
        print ('Invalid data in JSON config file.\n')
    else:
        #initialiaze variables
        username = dati['username'] #sets MQTT username
        password = dati['password'] #sets MQTT password
        Broker = dati["server"]     #sets MQTT broker IP address
        port = dati["port"]         #sets MQTT port 
        time_out = dati["timeout"]  #sets MQTT timeout
        topic = dati["topic"]       #sets MQTT Topic
        set_up_ok = True

if set_up_ok:
    try:
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
    except:
        print("\nSomething went wrong in connecting with the broker. Please check the config file and re-run.")
