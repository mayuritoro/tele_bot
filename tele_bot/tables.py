import pymysql
from config import mysql
from app import app

def create_table():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("create table if not exists user_info(mobile_no bigint not null primary key, name varchar(20) not null)")
    cursor.execute("create table if not exists user_plan(quote_id varchar(40) not null primary key, full_name varchar(20), mobile_no bigint, DOB DATE, gender varchar(10), education varchar(20), salary bigint, occuption_type varchar(20), policy_name varchar(20), coverage varchar(30))")
    conn.commit()
    cursor.close() 
    conn.close()