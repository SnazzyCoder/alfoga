from flask import Flask, render_template, redirect, request
from flaskext.mysql import MySQL
from models import mysql, shorten, is_url, url_of, app, randomize

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        long = request.form.get('URL')

        short = randomize()

        res = shorten(long, short)

        return render_template('index.html', short=short if res else 'error. Retry')

    print(request.remote_addr)
    return render_template('index.html')
    
@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        print("POST REcieved")
        print(request.get('name'), request.get('email'))
        return render_template('login.html')

    return render_template('login.html')


@app.route('/<route>/')
def redir(route):
    if is_url(route):
        return redirect(url_of(route), code=302)
    else:
        return render_template('404.html', code=404)


if __name__ == '__main__':
    app.run(port=5000, debug=True)