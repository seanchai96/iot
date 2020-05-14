import mysql
from mysql.connector import errorcode

def get_data(day="ALL", period="ALL"):
    config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }
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
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and WEEKDAY(last_update) = {}".format(day))
    elif period == "DAY" and day != "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and WEEKDAY(last_update)= {} and yearweek(DATE(last_update),1) = yearweek(curdate(),1)".format(day))
    elif period == "WEEKLY" and day != "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and WEEKDAY(last_update) = {} and last_update > NOW() - INTERVAL 7 DAY".format(day))
    elif period == "MONTHLY" and day != "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and WEEKDAY(last_update) = {} and last_update > NOW() - INTERVAL 30 DAY".format(day))
    elif day == "ALL" and period == "ALL":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6")
    elif day == "ALL" and period == "WEEKLY":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and last_update > NOW() - INTERVAL 7 DAY")
    elif day == "ALL" and period == "MONTHLY":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and last_update > NOW() - INTERVAL 30 DAY")
    elif day == "ALL" and period == "DAY":
        query = ("SELECT id,occ_status,last_update,WEEKDAY(last_update) as cur_day FROM occ_data WHERE extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and last_update > NOW() - INTERVAL 1 DAY")
    else: 
        return("INVALID SELECTION")
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
    
    #print("EMPTY COUNTER FOR", period, get_day(day), ":", empt)
    #print("OCCUPIED COUNTER FOR", period, get_day(day), ":", occ)
    #print("HOGGING COUNTER FOR", period, get_day(day), ":", hog)

    total_counts = empt + hog + occ

    #if empt == 0 or hog == 0 or occ == 0:
    #    if empt == 0 and hog != 0 and occ != 0:
    #        return("NO EMPT DATA")
    #    elif empt != 0 and hog == 0 and occ != 0: 
    #        return("NO HOG DATA")
    #    elif empt != 0 and hog != 0 and occ == 0:
    #        return("NO OCC DATA")
    #    else:
    #        return("NO DATA COLLECTED")
    #else:
    #    #print("PERCENT EMPTY: ", str(round(empt/total_counts*100,2)), "%")
    #    #print("PERCENT HOGGING: ", str(round(hog/total_counts*100,2)), "%")
    #    #print("PERCENT OCCUPIED: ", str(round(occ/total_counts*100,2)), "%")
    return ([empt,hog,occ])

def real_time():
    config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }

    occ = 0
    empt = 0
    hog = 0

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("SELECT * FROM occupancy")
    cursor.execute(query)
    for (id, occ_status, recent_run, last_update) in cursor:
        if (occ_status == "EMPTY"):
            empt += 1 
        elif (occ_status == "HOGGING"):
            hog += 1
        else:
            occ += 1 
    return ([empt, hog, occ])

def get_hourly(period="DAILY"):
    config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    if period == "DAILY":
        query = ("select id,occ_status, extract(hour from last_update) as Hour,extract(minute from (sec_to_time(time_to_sec(last_update)-time_to_sec(last_update)%(15*60)))) as Minute, count(*) as Count from occ_data where extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and DATE(last_update) = CURDATE() and time(last_update) <= '19:01:00' group by id, occ_status, extract(hour from last_update),Minute")
    elif period == "WEEKLY":
        query = ("select id,occ_status, extract(hour from last_update) as Hour,extract(minute from (sec_to_time(time_to_sec(last_update)-time_to_sec(last_update)%(15*60)))) as Minute, count(*) as Count from occ_data where extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and yearweek(DATE(last_update),1) = yearweek(curdate(),1) and time(last_update) <= '19:01:00' group by id, occ_status, extract(hour from last_update),Minute")
        #DATE(last_update) > date_sub(CURDATE(),interval 1 week)
    elif period == "ALL": 
        query = ("select id,occ_status, extract(hour from last_update) as Hour,extract(minute from (sec_to_time(time_to_sec(last_update)-time_to_sec(last_update)%(15*60)))) as Minute, count(*) as Count from occ_data where extract(hour from last_update) < 20 and extract(hour from last_update) > 6 and time(last_update) <= '19:01:00' group by id, occ_status, extract(hour from last_update),Minute")
    #query = ("select id,occ_status, extract(hour from last_update) as Hour , count(*) as Count from occ_data where extract(hour from last_update) < 20 and extract(hour from last_update) > 6 group by id, occ_status, extract(hour from last_update)")
    cursor.execute(query)

    last_index = -1
    

    occ_list_2 = [0]*49
    occ_list_7 = [0]*49

    emp_list_2 = [0]*49
    emp_list_7 = [0]*49

    hog_list_2 = [0]*49
    hog_list_7 = [0]*49

    final_occ = [0]*49
    final_emp = [0]*49
    final_hog = [0]*49

    for (id, occ_status, Hour, Minute, Count) in cursor:
        if id == "002":
            if occ_status == "OCCUPIED":
                if Minute == 0: 
                    occ_list_2[(Hour-7)*4] = Count
                    if (Hour-7)*4 > last_index:
                        last_index = (Hour-7)*4
                elif Minute == 15: 
                    occ_list_2[(Hour-7)*4+1] = Count 
                    if (Hour-7)*4+1 > last_index:
                        last_index = (Hour-7)*4+1
                elif Minute == 30: 
                    occ_list_2[(Hour-7)*4+2] = Count 
                    if (Hour-7)*4+2 > last_index:
                        last_index = (Hour-7)*4+2
                elif Minute == 45: 
                    occ_list_2[(Hour-7)*4+3] = Count 
                    if (Hour-7)*4+3 > last_index:
                        last_index = (Hour-7)*4+3
                
            elif occ_status == "EMPTY":
                if Minute == 0: 
                    emp_list_2[(Hour-7)*4] = Count
                    if (Hour-7)*4 > last_index:
                        last_index = (Hour-7)*4
                elif Minute == 15: 
                    emp_list_2[(Hour-7)*4+1] = Count 
                    if (Hour-7)*4+1 > last_index:
                        last_index = (Hour-7)*4+1
                elif Minute == 30: 
                    emp_list_2[(Hour-7)*4+2] = Count 
                    if (Hour-7)*4+2 > last_index:
                        last_index = (Hour-7)*4+2
                elif Minute == 45: 
                    emp_list_2[(Hour-7)*4+3] = Count 
                    if (Hour-7)*4+3 > last_index:
                        last_index = (Hour-7)*4+3
            elif occ_status == "HOGGING":
                if Minute == 0: 
                    hog_list_2[(Hour-7)*4] = Count
                    if (Hour-7)*4 > last_index:
                        last_index = (Hour-7)*4
                elif Minute == 15: 
                    hog_list_2[(Hour-7)*4+1] = Count 
                    if (Hour-7)*4+1 > last_index:
                        last_index = (Hour-7)*4+1
                elif Minute == 30: 
                    hog_list_2[(Hour-7)*4+2] = Count 
                    if (Hour-7)*4+2 > last_index:
                        last_index = (Hour-7)*4+2
                elif Minute == 45: 
                    hog_list_2[(Hour-7)*4+3] = Count 
                    if (Hour-7)*4+3 > last_index:
                        last_index = (Hour-7)*4+3
            
        elif id == "007":
            if occ_status == "OCCUPIED":
                if Minute == 0: 
                    occ_list_7[(Hour-7)*4] = Count
                    if (Hour-7)*4 > last_index:
                        last_index = (Hour-7)*4
                elif Minute == 15: 
                    occ_list_7[(Hour-7)*4+1] = Count 
                    if (Hour-7)*4+1 > last_index:
                        last_index = (Hour-7)*4+1
                elif Minute == 30: 
                    occ_list_7[(Hour-7)*4+2] = Count 
                    if (Hour-7)*4+2 > last_index:
                        last_index = (Hour-7)*4+2
                elif Minute == 45: 
                    occ_list_7[(Hour-7)*4+3] = Count 
                    if (Hour-7)*4+3 > last_index:
                        last_index = (Hour-7)*4+3
                
            elif occ_status == "EMPTY":
                if Minute == 0: 
                    emp_list_7[(Hour-7)*4] = Count
                    if (Hour-7)*4 > last_index:
                        last_index = (Hour-7)*4
                elif Minute == 15: 
                    emp_list_7[(Hour-7)*4+1] = Count 
                    if (Hour-7)*4+1 > last_index:
                        last_index = (Hour-7)*4+1
                elif Minute == 30: 
                    emp_list_7[(Hour-7)*4+2] = Count 
                    if (Hour-7)*4+2 > last_index:
                        last_index = (Hour-7)*4+2
                elif Minute == 45: 
                    emp_list_7[(Hour-7)*4+3] = Count 
                    if (Hour-7)*4+3 > last_index:
                        last_index = (Hour-7)*4+3
            elif occ_status == "HOGGING":
                if Minute == 0: 
                    hog_list_7[(Hour-7)*4] = Count
                    if (Hour-7)*4 > last_index:
                        last_index = (Hour-7)*4
                elif Minute == 15: 
                    hog_list_7[(Hour-7)*4+1] = Count 
                    if (Hour-7)*4+1 > last_index:
                        last_index = (Hour-7)*4+1
                elif Minute == 30: 
                    hog_list_7[(Hour-7)*4+2] = Count 
                    if (Hour-7)*4+2 > last_index:
                        last_index = (Hour-7)*4+2
                elif Minute == 45: 
                    hog_list_7[(Hour-7)*4+3] = Count 
                    if (Hour-7)*4+3 > last_index:
                        last_index = (Hour-7)*4+3

    for i in range(len(occ_list_2)):
        if emp_list_2[i] > hog_list_2[i] and emp_list_2[i] > occ_list_2[i]:
            final_emp[i] += 1 
        elif hog_list_2[i] > emp_list_2[i] and hog_list_2[i] > occ_list_2[i]:
            final_hog[i] += 1 
        elif occ_list_2[i] > emp_list_2[i] and occ_list_2[i] > hog_list_2[i]:
            final_occ[i] += 1
        
        if emp_list_7[i] > hog_list_7[i] and emp_list_7[i] > occ_list_7[i]:
            final_emp[i] += 1 
        elif hog_list_7[i] > emp_list_7[i] and hog_list_7[i] > occ_list_7[i]:
            final_hog[i] += 1 
        elif occ_list_7[i] > emp_list_7[i] and occ_list_7[i] > hog_list_7[i]:
            final_occ[i] += 1

    if last_index+1 < len(final_emp):
        for i in range(last_index+1, len(final_emp)):
            if final_emp[i] == 0: 
                final_emp[i] = None
            if final_occ[i] == 0: 
                final_occ[i] = None
            if final_hog[i] == 0:
                final_hog[i] = None
    return [final_emp, final_occ, final_hog]

def get_pic():
    config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }

    mb2 = []
    mb7 = []

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("SELECT * FROM occupancy")
    cursor.execute(query)
    for (id, occ_status, recent_run, last_update) in cursor:
        if id == "002":
            mb2.append(occ_status)
        elif id == "007":
            mb7.append(occ_status)
    return ([mb2,mb7])