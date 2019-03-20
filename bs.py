import mysql.connector
import time

from string import ascii_lowercase

def get_db_server():
    return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            buffered=True)

def get_db():
    return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="bs",
            buffered=True)

def create_database():
    conn = get_db_server()
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS bs;")
    finally:
        conn.commit()
        conn.close()


def init_db():
    # think the status should be a foreign key to a status table with options
    # period_id should be a foreign key
    jobs_ddl = ("CREATE TABLE IF NOT EXISTS "
                 "jobs ("
                 "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                 "status VARCHAR(32),"
                 "final_status VARCHAR(32),"
                 "period_id INT NOT NULL,"
                 "start DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,"
                 "end DATETIME,"
                 "task_id INT);")

    conn = get_db()
    try:
        cursor = conn.cursor() 
        cursor.execute(jobs_ddl)
    finally:
        conn.commit()
        conn.close()

def get_active_jobs():
    active_jobs_query = ("SELECT * FROM jobs "
                         "WHERE state")
    print("End get_active_jobs")
    return []

def bs():
    create_db()
    init_db()
    while true:
        active_jobs = get_active_jobs()
        for job in active_jobs:
            print(job)
        time.sleep(300) 
