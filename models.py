from flaskext.mysql import MySQL
from flask import Flask
import string
import random

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = "remotemysql.com"
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = "d2amZpLtuY"
app.config['MYSQL_DATABASE_PASSWORD'] = 'uWcVsX9Iqo'
app.config['MYSQL_DATABASE_DB'] = "d2amZpLtuY"
mysql = MySQL()
mysql.init_app(app)


def return_single(cmd):
    conn =  mysql.connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute(cmd)
    except Exception as e:
        print("!!!error", e)
        return False
    finally:
        conn.close()
        
    return cursor.fetchone()[0]

def is_url(url):
    return return_single(f'select count(*) from urls where shorturl="{url}"') >= 1

def url_of(short):
    return return_single(f"SELECT longurl from urls where shorturl='{short}'")

def shorten(long, short):
    conn =  mysql.connect()
    cursor = conn.cursor()
    
    try:
        res = cursor.execute("INSERT INTO urls (longurl, shorturl) values (%s, %s)", (long, short))
        conn.commit()
    except Exception as e:
        print("!!!error", e)
        return False
    finally:
        conn.close()
        
    return res == 1

def randomize(includes: list=[string.ascii_lowercase, string.ascii_uppercase, string.digits]):

    return ''.join([[i for i in random.choice([i for i in random.choice(includes)])][0] for _ in range(6)])