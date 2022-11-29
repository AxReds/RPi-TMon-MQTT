

# import
import time
import paho.mqtt.client as mqtt #Import Paho MQTT Library
import json #Import json library


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
        server = dati["server"]
        port = dati["port"]
        time_out = dati["timeout"]


# broker IP address
Broker = server

# publish topic
topic = "test/topic"

# on connect function
def on_connect(client, userdata, flags, rc) :
    print("Client che invia messaggi connesso con codice: " + str(rc))

# instantiate paho MQTT client
client = mqtt.Client()
#set usrname and password
client.username_pw_set(username, password)

# add on_connect function to on_connect event
client.on_connect = on_connect

# connect paho client to mosquitto broker (IP, port, timeout)
client.connect(Broker, port, time_out)

# put client's loop in background
client.loop_start()

# send messages every 2 seconds
i = 0
while True:
    i = i + 1
    client.publish(topic, "Test: " + str(i))
    time.sleep(2)


