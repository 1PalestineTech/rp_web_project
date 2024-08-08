
from flask import Flask, render_template,request,redirect,session
import json
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import threading
import sqlite3
from src.utils import apology
db =sqlite3.connect('data.db')
# import shortuuid
# shortuuid.ShortUUID().random(length=20)
#
#
app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/bot')
def bot():

    return render_template("blog.html")
@app.route('/cultures')
def culture():

    return render_template("destinations.html")
@app.route('/photography')
def hotography():

    return render_template("mystories.html")
@app.route('/articles')
def articles():

    return render_template("single.html")
@app.route('/about')
def about():

    return render_template("about.html")

@app.route('/admin_login', methods = ['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        cursor = db.execute("SELECT * FROM admins WHERE username = (?) ",(username,))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else :
        if not (session.get("user_id") is None):
            return redirect('/')
        else:
            return render_template("admin_login.html")

@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/')
    
if __name__ == '__main__':
   app.run(host='0.0.0.0',port = "5000")

