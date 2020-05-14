import pandas as pd 
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

config = {
        'user': '',
        'password': '',
        'host': 'database-1.cyyaapqeneuy.ap-southeast-1.rds.amazonaws.com',
        'database': 'database-1',
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
        print("success!")
        cnx.close()
    
connect_sql()

def write_to_sql(user,database, sql_stm):
    cnx = mysqlconnector.connect(user=user, database=database)
    cursor = cnx.cursor()

    cur_time = datetime.now()

    add_data = sql_stm