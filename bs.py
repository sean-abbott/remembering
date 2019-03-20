import os
import mysql.connector
import random
import sys
import time

from string import ascii_lowercase

DB_HOST=os.environ.get('BS_DB_HOST', 'localhost')
SLEEP_TIME=int(os.environ.get('BS_SLEEP_TIME', 10))

def get_db_server(host=DB_HOST):
    return mysql.connector.connect(
            host=host,
            user="root",
            passwd="password",
            buffered=True)

def get_db(host=DB_HOST):
    return mysql.connector.connect(
            host=host,
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
                 "queued DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,"
                 "start DATETIME,"
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
                         "WHERE status NOT IN "
                         "('completed', 'errored');")
    conn = get_db()
    result = []
    try:
        cursor = conn.cursor(dictionary=True) 
        cursor.execute(active_jobs_query)
        result = cursor.fetchall()
    finally:
        conn.commit()
        conn.close()
    return result

def random_do_update(chance):
    '''Return True $chance percentage of the time

    Inputs:
    chance:int
    '''
    return random.randint(0, 99) < chance

def update_job_status(job_id, time_field, new_status):
    update_query = ("UPDATE jobs "
                    "set status = '{}',"
                    "{} = NOW() "
                    "where id = {};").format(new_status, time_field, job_id)
    conn = get_db()
    result = None
    try:
        cursor = conn.cursor(dictionary=True) 
        cursor.execute(update_query)
        result = cursor.lastrowid
        print('job {} marked {}'.format(job_id, new_status))
    finally:
        conn.commit()
        conn.close()
    return result


def bs():
    create_database()
    init_db()
    while True:
        active_jobs = get_active_jobs()
        for job in active_jobs:
            if job['status'] == 'queued':
                if random_do_update(80):
                    update_job_status(job['id'], 'start',  'running')
            if job['status'] == 'running':
                if random_do_update(50):
                    update_job_status(job['id'], 'end',  'complete')
                elif random_do_update(10):
                    update_job_status(job['id'], 'end',  'errored')


        print('Status updates complete. Sleeping for {} seconds'.format(SLEEP_TIME))
        sys.stdout.flush()
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    print("Starting batch simulator...")
    bs()
