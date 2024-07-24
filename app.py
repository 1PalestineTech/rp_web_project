
from flask import Flask, render_template,make_response,request,redirect
import json
import threading
app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():

    return render_template("index.html")
@app.route('/bot')
def bot():

    return render_template("blog.html")
@app.route('/culture')
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
    

if __name__ == '__main__':
   app.run(host='0.0.0.0',port = "5000")

