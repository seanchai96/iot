# Import paho mqtt client module # 
import paho.mqtt.client as mqtt
# Import time module to call time functions # 
import time 
from mysql_data import connect_sql, write_to_sql
import ast

print("PAHO SCRIPT RUNNING")

def on_connect(client, userdata, flags, rc): # Function that is called when client is connected to the broker # 
    if rc == 0: # rc 0 --> Connection successful
        print("Connection to Broker Established")
        print("")
    else: 
        print("Connection to Broker Unsuccessful. Result code: ", str(rc))

def on_message(client, userdata, msg): # Function that is called when a message is received by paho from the server #
    message = msg.payload.decode("utf-8")
    print("DATA RECEIVED: " + str(message)) 
    print("")
    message = ast.literal_eval(message)
    pir_data = message['pir']                       # CHANGE MESSAGES RECEIVED HERE #
    #ultrasonic_seat = message['ultrasonic_seat']              # CHANGE MESSAGES RECEIVED HERE #
    ultrasonic_table = message['ultrasonic_table']
    mbid = message['id']

    print("MICROBIT ID:" + mbid)
    print("PIR STATUS: " + pir_data)
    #print("ULTRASONIC SEAT STATUS: ", ultrasonic_seat)
    print("ULTRASONIC TABLE STATUS: ", ultrasonic_table)
    print("")

    ############################################### DATABASE PORTION ########################################

    config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }
    
    write_to_sql(config, mbid, pir_data, ultrasonic_table)#ultrasonic_seat, ultrasonic_table) # Write to SQL Server Connection # 
    print("Written to Database!")

    ############################################## END OF DATABASE PORTION ###################################

broker = "broker.hivemq.com"

client = mqtt.Client("noiseboys-pir") # Creates an instance of client with client ID = "noiseboys-pir"
client.on_connect = on_connect # Define callback function for successful connection 
client.on_message = on_message # Define callback function for receiving of messages

client.connect(broker, 1883, 60) # Connect client to (broker-address, port, keep-alive-time)

client.subscribe("noiseboys/pir")

client.loop_forever()

