from __future__ import print_function
import pandas as pd 
import mysql
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

config = {
        'user': 'admin',
        'password': 'RhiDa3K0ocufgmdtMyQV',
        'host': 'newiotdb.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'iot_db',
        'port': 3306,
        'raise_on_warnings': True
    }
    
def connect_sql(config):

    try:
      cnx = mysql.connector.connect(**config)

    except mysql.connector.Error as err:

      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")

      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")

      else:
        print(err)

    else:
        print("Connection to Database was Established!")
        cnx.close()
    
#connect_sql(config)

def write_to_sql(config, mbid, pir_data, ultrasonic_table):#ultrasonic_seat, ultrasonic_table):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    sql_stmt = ("INSERT INTO iot "
                "(id, pir, ultrasonic_table)" # add one more ultrasonic_seat
                "VALUES (%s, %s, %s)" ) # add one more %s if 3 sensors

    ins_data = (mbid, pir_data, ultrasonic_table) #ultrasonic_seat, ultrasonic_table)

    #cur_time = datetime.now()
    execute_sql = cursor.execute(sql_stmt, ins_data)
    cnx.commit()
    #print("Write to SQL successful.")
    cursor.close()
    cnx.close()
  
def query_sql(config, table, mbid):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("SELECT * FROM %s WHERE id= %s")

    ins_data = (table, mbid)

    cursor.execute(query, ins_data)

    for(id, pir, ultrasonic_table, time_col) in cursor: # add one more ultrasonic_seat
      print("id: {}, pir: {}, ultrasonic:{}, time_col{}". format(
        id, pir, ultrasonic_table, time_col))  #add one more ultrasonic_seat
    
    cursor.close()
    cnx.close()



