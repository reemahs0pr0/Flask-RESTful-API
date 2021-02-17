import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

def insert_jobs():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="jinder"
     )
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT * FROM jobs"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    jobsData = pd.read_csv('fullmonsters.csv')
    engine = create_engine('mysql+pymysql://root:password@localhost:3306/jinder')
    if mycursor.rowcount == 0 :
        jobsData.to_sql('jobs', con=engine, if_exists='append', index=True, index_label='id')
    else:
        sql = "DELETE FROM jobs"
        mycursor.execute(sql)
        mydb.commit()
        old_jobs = pd.DataFrame(myresult, columns=["id", "companyName", "jobAppUrl", \
                                                   "jobDescription", "jobTitle", "skills"])
        updated_jobs = pd.concat([jobsData, old_jobs])
        updated_jobs = updated_jobs.reset_index()
        updated_jobs = updated_jobs.drop(columns=["index", "id"])
        updated_jobs.to_sql('jobs', con=engine, if_exists='append', index=True, index_label='id')
    mycursor.close()
    mydb.close()