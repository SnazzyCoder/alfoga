from flask import Flask, render_template, redirect, request
import string

app = Flask(__name__)

app.config('')

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('URL')

        short = ''.join([[i for i in random.choice([i for i in random.choice([string.ascii_lowercase, string.ascii_uppercase, string.digits])])][0] for _ in range(6)])



        return render_template('index.html', short=short)
    return render_template('index.html')