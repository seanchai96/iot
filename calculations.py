import mysql
from mysql.connector import errorcode

def get_day(day):
    if day != "ALL":
        day = int(day)
        if day == 0:
            return "Monday"
        elif day == 1: 
            return "Tuesday"
        elif day == 2: 
            return "Wednesday"
        elif day == 3:
            return "Thursday"
        elif day == 4: 
            return "Friday"
        elif day == 5: 
            return "Saturday"
        elif day == 6: 
            return "Sunday"
    else:
        return day

config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }

def get_data(day="ALL", period="ALL"):
    period = period.upper()
    # DAY = INTEGER/ ALL, PERIOD = WEEKLY/MONTHLY/ALL
    # COMBINATIONS: 
        #get_data(integer, "ALL") <- returns data for specified day for ALL DATA 
        #get_data(integer, "WEEKLY") <- returns data for specified day for the past week 
        #get_data(integer, "MONTHLY") <- returns data for specified day for the past month 
        #get_data("ALL", "ALL") <- returns data for ALL DAYS FOR ALL DATA 
        #get_data("ALL", "WEEKLY") <- returns data for ALL DAYS for the past week 
        #get_data("ALL", "MONTHLY") <- returns data for ALL DAYS for the past month 
        #get_data("ALL", "DAY") <- returns data for ALL DAYS for the past day 

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    if period == "ALL" and day != "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE WEEKDAY(last_update) = {}".format(day))
    elif period == "WEEKLY" and day != "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE WEEKDAY(last_update) = {} and last_update > NOW() - INTERVAL 7 DAY".format(day))
    elif period == "MONTHLY" and day != "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE WEEKDAY(last_update) = {} and last_update > NOW() - INTERVAL 30 DAY".format(day))
    elif day == "ALL" and period == "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data")
    elif day == "ALL" and period == "WEEKLY":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE last_update > NOW() - INTERVAL 7 DAY")
    elif day == "ALL" and period == "MONTHLY":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE last_update > NOW() - INTERVAL 30 DAY")
    elif day == "ALL" and period == "DAY":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE last_update > NOW() - INTERVAL 1 DAY")
    else: 
        print ("INVALID SELECTION")
        return()
    cursor.execute(query)
    

    empt = 0 
    hog = 0 
    occ = 0 

    for (id,occ_status, last_update, cur_day) in cursor: 
        if occ_status == "EMPTY":
            empt += 1
        elif occ_status == "HOGGING":
            hog += 1 
        elif occ_status == "OCCUPIED":
            occ += 1 
    
    print("EMPTY COUNTER FOR", period, get_day(day), ":", empt)
    print("OCCUPIED COUNTER FOR", period, get_day(day), ":", occ)
    print("HOGGING COUNTER FOR", period, get_day(day), ":", hog)

    total_counts = empt + hog + occ

    if empt == 0 or hog == 0 or occ == 0:
        if empt == 0 and hog != 0 and occ != 0:
            print("NO EMPT DATA")
        elif empt != 0 and hog == 0 and occ != 0: 
            print("NO HOG DATA")
        elif empt != 0 and hog != 0 and occ == 0:
            print("NO OCC DATA")
        else:
            print("NO DATA COLLECTED")
    else:
        print("PERCENT EMPTY: ", str(round(empt/total_counts*100,2)), "%")
        print("PERCENT HOGGING: ", str(round(hog/total_counts*100,2)), "%")
        print("PERCENT OCCUPIED: ", str(round(occ/total_counts*100,2)), "%")

get_data(day="ALL", period="ALL")


