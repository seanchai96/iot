import mysql
import time
from mysql.connector import errorcode
from mysql_data import query_sql
from datetime import datetime

time.sleep(65)

print("SQL SCRIPT STARTING")

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
while i <= 100: 
    print("TIME NOW: ", datetime.now())
    for mbid in id_list:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        #now = datetime.strptime('2020-03-02 18:26:29', "%Y-%m-%d %H:%M:%S")
        #datetime.now()

        query = ("SELECT * FROM iot WHERE id= {} and time_col > NOW() - INTERVAL 1 MINUTE".format(mbid))

        cursor.execute(query)

        pir_counter = 0
        us = -1000
        us_counter = -1
        spike_counter = -1
        pir_readings = []
        hog_counter = 0
        last_ustable_reading = 100

        for (id, pir, ultrasonic_table, time_col) in cursor: #ultrasonic_seat, 
            #get_time = datetime.strptime(time_col, "%Y-%m-%d %H:%M:%S")
            #time_difference = (now - time_col).total_seconds()
            #if time_difference <= 60 and time_difference >=0: # Change Time Period Here #

            pir_readings.append(pir)

            if pir == "MOVEMENT":
                pir_counter += 1

            #us_diff = abs(int(ultrasonic_seat) - us)
            #us = int(ultrasonic_seat)
            #if (us_diff >= 15):                          # Change Ultrasonic Threshold Here # 
            #    us_counter += 1
            
            last_ustable_reading = int(ultrasonic_table) # Get the last reading for the ultrasonic sensor for table # 

            #if (us_diff >= 10):
            #    spike_counter += 1

        pir_readings_last30 = pir_readings[-10:]               # Change threshold for number of readings to take into account for PIR sensor Occupied to Empty #
        pir_readings_first30 = pir_readings[0:10]
        pir_readings_last60 = pir_readings[-20:]

        print("Movements detected: ",pir_counter)
        #print("Ultrasonic Seat diff >= 15: ", us_counter)
        print("Ultrasonic Value: ", last_ustable_reading)
        #print("Ultrasonic Seat diff >= 20: ", spike_counter)
        #print("FIRST 30S of PIR READINGS: ")
        #print(pir_readings_first30)
        #print("LAST 30S OF PIR READINGS: ")
        #print(pir_readings_last30)
        #print("LAST 60S OF PIR READINGS: ")
        #print(pir_readings_last60)
        


        query = ("SELECT * FROM occupancy WHERE id= {}".format(mbid))
        cursor = cnx.cursor()
        cursor.execute(query)

        for (id, occ_status, recent_run, last_update) in cursor:
            print(id, " is ", occ_status)
    
            query = ("SELECT * FROM iot WHERE id= {} and time_col > NOW() - INTERVAL 5 MINUTE".format(mbid))
                
            cursor.execute(query)
            for (id, pir, ultrasonic_table, time_col) in cursor:
                if pir == "MOVEMENT":
                    hog_counter += 1
            print("HOG COUNTER: ", hog_counter)

            if (hog_counter <= 15 and last_ustable_reading <= 50):
                query = ("SELECT * FROM occupancy WHERE id={}".format(mbid))
                cursor.execute(query)
                for (id, occ_status,recent_run, last_update) in cursor:
                    if occ_status != "HOGGING":
                        stmt = ("UPDATE occupancy SET occ_status = 'HOGGING', recent_run = CURRENT_TIMESTAMP WHERE id={}".format(mbid))
                        print("current occ_status set to 'HOGGING'")
                        cursor = cnx.cursor()
                        cursor.execute(stmt)
                        cnx.commit()

                        stmt = ("INSERT INTO occ_data (id, occ_status) VALUES ({}, {})".format(mbid, "'HOGGING'"))
                        cursor = cnx.cursor()
                        cursor.execute(stmt)
                        cnx.commit()

                    else:
                        if (pir_counter >= 1 and last_ustable_reading <= 50):
                            stmt = ("UPDATE occupancy SET occ_status = 'OCCUPIED', recent_run = CURRENT_TIMESTAMP WHERE id={}".format(mbid))
                            print("current occ_status set to 'OCCUPIED'")
                            cursor = cnx.cursor()
                            cursor.execute(stmt)
                            cnx.commit()    
                            stmt = ("INSERT INTO occ_data (id, occ_status) VALUES ({}, {})".format(mbid, "'OCCUPIED'"))
                            cursor = cnx.cursor()
                            cursor.execute(stmt)
                            cnx.commit() 
                        else: 
                            stmt = ("UPDATE occupancy SET occ_status = 'HOGGING', recent_run = CURRENT_TIMESTAMP WHERE id={}".format(mbid))
                            print("current occ_status set to 'HOGGING'")
                            cursor = cnx.cursor()
                            cursor.execute(stmt)
                            cnx.commit()

                            stmt = ("INSERT INTO occ_data (id, occ_status) VALUES ({}, {})".format(mbid, "'HOGGING'"))
                            cursor = cnx.cursor()
                            cursor.execute(stmt)
                            cnx.commit()
            elif (pir_counter >= 2 and last_ustable_reading <= 50):
                stmt = ("UPDATE occupancy SET occ_status = 'OCCUPIED', recent_run = CURRENT_TIMESTAMP WHERE id={}".format(mbid))
                print("current occ_status set to 'OCCUPIED'")
                cursor = cnx.cursor()
                cursor.execute(stmt)
                cnx.commit()    
                stmt = ("INSERT INTO occ_data (id, occ_status) VALUES ({}, {})".format(mbid, "'OCCUPIED'"))
                cursor = cnx.cursor()
                cursor.execute(stmt)
                cnx.commit()    
            #if occ_status == "EMPTY":
                #if (pir_counter >= 5 and us_counter >= 1) or (pir_counter > 7):               # Change PIR Movement Threshold Here #
            
            #if occ_status == "OCCUPIED" and pir_readings != []:
                #if ((pir_readings_last30.count("MOVEMENT") <= 1 and us_counter >= 1 and pir_readings_first30.count("MOVEMENT") > 3) or (pir_readings_last60.count("MOVEMENT") <= 3)):
                #if ((pir_readings_first.count(pir_readings_first[0]) == len(pir_readings_first) and us_counter >= 1) or (pir_readings_second.count(pir_readings_second[0]) == len(pir_readings_second))):            # Change threshold for Ultrasonic Spike Counter # 
            elif (pir_readings_last30.count("MOVEMENT") <= 1 and last_ustable_reading > 50):
                #if (last_ustable_reading < 40):
                stmt = ("UPDATE occupancy SET occ_status = 'EMPTY', recent_run = CURRENT_TIMESTAMP WHERE id={}".format(mbid))
                print("current occ_status set to 'EMPTY'")
                cursor = cnx.cursor()
                cursor.execute(stmt)
                cnx.commit()

                stmt = ("INSERT INTO occ_data (id, occ_status) VALUES ({}, {})".format(mbid, "'EMPTY'"))
                cursor = cnx.cursor()
                cursor.execute(stmt)
                cnx.commit()

        cursor.close()

        cnx.close()

    for n in range(60):
        time.sleep(1)
        print (n)
        n += 1
    
    print("SQL SCRIPT RAN")
