import mysql.connector
import os

DB_HOST=os.environ.get('BS_DB_HOST', 'localhost')

def get_db(host='localhost'):
    return mysql.connector.connect(
            host=host,
            user="root",
            passwd="password",
            database="bs",
            buffered=True)

def queue(job_id, period):
    '''Returns the id of the task'''
    conn = get_db(DB_HOST)
    queue_sql = ("insert into jobs "
                 "(status, period_id, task_id) "
                 "values ('queued', {}, {});").format(period, job_id)
    print(queue_sql)
    result = -1
    try:
        cursor = conn.cursor()
        cursor.execute(queue_sql)
        result = cursor.lastrowid
    finally:
        conn.commit()
        conn.close()
    return result

def status(task_id):
    conn = get_db(DB_HOST)
    query = "select * from jobs where id = {}".format(task_id)
    result = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchone()
    finally:
        conn.commit()
        conn.close()
    return result

def delete(task_id):
    conn = get_db(DB_HOST)
    # better would be to check if the job exists first.
    # sql will return the same either way, so hard to validate without checking
    # before and after
    query = 'delete from jobs where id = {};'.format(task_id)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
    finally:
        conn.commit()
        conn.close()
