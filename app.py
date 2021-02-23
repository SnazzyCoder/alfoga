from flask import Flask, render_template, redirect, request
from flaskext.mysql import MySQL
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


def return_one(cmd):
    conn =  mysql.connect()
    cursor = conn.cursor()
    
    try:
        res = cursor.execute(cmd)
    except Exception as e:
        print("!!!error", e)
        return False
    finally:
        conn.close()
        
    return cursor.fetchone()[0]

def is_url(url):
    return return_one(f'select count(*) from urls where shorturl="{url}"') >= 1

def url_of(short):
    return return_one(f"SELECT longurl from urls where shorturl='{short}'")

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

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long = request.form.get('URL')

        short = ''.join([[i for i in random.choice([i for i in random.choice([string.ascii_lowercase, string.ascii_uppercase, string.digits])])][0] for _ in range(6)])

        res = shorten(long, short)

        return render_template('index.html', short=short if res else 'error. Retry')
    return render_template('index.html')
    
@app.route('/<route>')
def redir(route):
    if is_url(route):
        return redirect(url_of(route), code=302)
    else:
        return render_template('404.html', code=404)