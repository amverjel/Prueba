import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        conn = sqlite3.connect('elAlcaravan.db')
        print("Conexión OK.")
        return conn
    except Error:
        print(Error)

def sql_select_productos(sql):
    sql = sql
    conn = sql_connection()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    datos = cursoObj.fetchall() 
    return datos

def sql_insert_productos(sql):
    sql = sql
    conn = sql_connection()
    cursorObj = conn.cursor()
    cursorObj.execute(sql)
    conn.commit()
    conn.close()