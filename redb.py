import mysql.connector

from string import ascii_lowercase

def get_db():
    return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="dag",
            buffered=True)


def init_db():
    nodes_ddl = ("CREATE TABLE IF NOT EXISTS "
                 "nodes ("
                 "node_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                 "node_name VARCHAR(255) NOT NULL UNIQUE);")

    relations_ddl = ("CREATE TABLE IF NOT EXISTS relations ("
                     "parent_id INTEGER NOT NULL,"
                     "child_id INTEGER NOT NULL,"
                     "PRIMARY KEY (parent_id, child_id));")

    conn = get_db()
    try:
        cursor = conn.cursor() 
        cursor.execute(nodes_ddl)
        cursor.execute(relations_ddl)
    finally:
        conn.commit()
        conn.close()

def get_inmem_dag()
    conn = get_db()
    try:
        cursor = conn.cursor()
        print("more to do")
    finally:
        conn.close()

def insert_node(cursor, node_name):
    query = ("insert into nodes (node_name) values ('{}')".format(node_name))
    cursor.execute(query)

def insert_relation(cursor, child, parent):
    cid_query = "select node_id from nodes where node_name = '{}';".format(child)
    pid_query = "select node_id from nodes where node_name = '{}';".format(parent)
    cursor.execute(cid_query)
    cid = cursor.fetchone()[0]
    cursor.execute(pid_query)
    pid = cursor.fetchone()[0]

    insert_query = 'insert into relations (child_id, parent_id) values ({}, {});'.format(cid, pid)
    cursor.execute(insert_query)

def init_simple_test():
    conn = get_db()
    try:
        cursor = conn.cursor()
        for l in ascii_lowercase[:5]:
            insert_node(cursor, l)
        insert_relation(cursor, 'e', 'd')
        insert_relation(cursor, 'd', 'b')
        insert_relation(cursor, 'd', 'c')
        insert_relation(cursor, 'b', 'a')
        insert_relation(cursor, 'c', 'a')
    finally:
        conn.commit()
        conn.close()
