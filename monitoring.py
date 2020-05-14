import mysql
import time
from mysql.connector import errorcode
from datetime import datetime

#time.sleep(3600)

config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }

id_list = ["'002'", "'007'"]

i = 0

while i < 100:

    log_dic = {'002':[], '007':[]}

    cur_time = datetime.now()

    
    paho_counter = 0 
    sql_counter = 0 

    for mbid in id_list: 

        prev = -1000

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = ("SELECT id, time_col, time_to_sec(time_col) as seconds FROM iot WHERE id = {} and time_col > NOW() - INTERVAL 60 MINUTE".format(mbid))
        cursor.execute(query)


        for (id, time_col, seconds) in cursor:

            if prev == -1000:
                prev = seconds 
            else: 
                if seconds == prev or seconds-prev > abs(30): 
                    paho_counter += 1 
                    log_dic[id].append([str(time_col), "Failed to collect data at " + str(time_col) + " (PAHO-MQTT to MYSQL SERVER)"])
                prev = seconds 

        prev = -1000 

        query = ("SELECT id, last_update, time_to_sec(last_update) as seconds FROM occ_data WHERE id= {} and last_update > NOW() - INTERVAL 60 MINUTE".format(mbid))
        cursor.execute(query)

        for (id, last_update, seconds) in cursor: 

            if  prev == -1000:
                prev = seconds 
            else: 
                if seconds == prev or seconds-prev > abs(100): 
                    sql_counter += 1 
                    log_dic[id].append([str(last_update), "Failed to updated occupancy status at " + str(last_update) + " (MYSQL SCRIPT)"]) 
                prev = seconds 

    print("sql",sql_counter)
    print("paho", paho_counter)
    
    for key,value in log_dic.items():
        for val in value: 
            print("\n", key, val)


    
