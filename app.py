
from flask import Flask, render_template,request,redirect,session
import json
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import threading
import sqlite3
import shortuuid
import os.path
import os
from src.utils import login_required,head_admin
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route('/')
@app.route('/index')
def index():
    db = sqlite3.connect('web_data.db')
    cursor = db.execute("SELECT * FROM articles ORDER BY date DESC LIMIT 4")
    articles = cursor.fetchall()
    cursor = db.execute("SELECT * FROM cultures ORDER BY date DESC LIMIT 4")
    cultures = cursor.fetchall()
    return render_template("index.html",articles = articles,cultures=cultures)

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/admin_login', methods = ['GET','POST'])
def login():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", top=403, bottom="must provide username",url=request.path),403 

        elif not request.form.get("password"):
            return render_template("error.html", top=403, bottom="must provide password",url=request.path),403 
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        cursor = db.execute("SELECT * FROM admins WHERE username = (?) ",(username,))
        rows = cursor.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2],password):
            return render_template("error.html", top=403, bottom="invalid username and/or password",url=request.path),403 
        session["user_id"] = rows[0][0]
        return redirect("/")
    else :
        if not (session.get("user_id") is None):
            return redirect('/')
        else:
            return render_template("admin_login.html")

@app.route('/change_password', methods = ['GET','POST'])
@login_required
def change_password():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        if not request.form.get("old_password"):
            return render_template("error.html", top=403, bottom="must provide old password",url=request.path),403 

        elif not request.form.get("new_password"):
            return render_template("error.html", top=403, bottom="must provide the new password",url=request.path),403 
        old_password = request.form.get('old_password').strip()
        new_password = request.form.get('new_password').strip()
        cursor = db.execute("SELECT * FROM admins WHERE id = (?) ",(session.get("user_id"),))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][2],old_password):
            return render_template("error.html", top=403, bottom="wrong password",url=request.path),403
        hs=generate_password_hash(new_password) 
        db.execute("UPDATE admins SET password = (?) WHERE id = (?)",(hs,session.get("user_id")))
        db.commit()
        
        return redirect("/admin_control")
    else :

        return render_template("change_password.html")
@app.route('/add_admin', methods = ['GET','POST'])
@login_required
@head_admin
def add_admin():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if not request.form.get("username"):
            return render_template("error.html", top=403, bottom="must provide username",url=request.path),403 

        elif not request.form.get("password"):
            return render_template("error.html", top=403, bottom="must provide password",url=request.path),403 
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM admins WHERE username = (?) ",(username,))
        rows = cursor.fetchall()
        if len(rows)>0:
            return render_template("error.html", top=403, bottom="username aleardy exist",url=request.path),403 
        id = shortuuid.ShortUUID().random(length=20)
        hs=generate_password_hash(password)
        db.execute("INSERT INTO admins (id,username,password) VALUES ((?),(?),(?)) ",(id, username, hs))
        db.commit()
        return redirect('/admin_control')
    else:
        return render_template("add_admin.html")
@app.route('/remove_admin', methods = ['GET','POST'])
@login_required
@head_admin
def remove_admin():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        
        ids = request.form.getlist('admins')
        for id in ids:
            cursor = db.execute("SELECT * FROM head_admins WHERE id = (?) ",(id,))
            rows = cursor.fetchall()
            if len(rows)!=1:
                db.execute("DELETE FROM admins WHERE id = (?) ",(id,))
                db.commit()
        return redirect('/remove_admin')
    
    cursor = db.execute("SELECT * from admins where id not in (select id from head_admins) ")
    rows = cursor.fetchall()
    return render_template("remove_admin.html",admins=rows)
@app.route('/add_item', methods = ['POST'])
@login_required
def add_item():
    if not request.form.get('type'):
        return render_template("error.html", top=403, bottom="Select type",url=request.path),403 

    elif not request.files.getlist("images"):
        return render_template("error.html", top=403, bottom="pls provide 1 image or more",url=request.path),403 
    elif not request.files['file'] :
        return render_template("error.html", top=403, bottom="pls select the text file",url=request.path),403 
    elif not request.form.get('title') :
        return render_template("error.html", top=403, bottom="pls select the text file",url=request.path),403
    elif not request.form.get('desciption') :
        return render_template("error.html", top=403, bottom="pls provide desciption ",url=request.path),403
    id = str(shortuuid.ShortUUID(alphabet="013456789").random(length=20))
    dir=request.form.get('type').strip()
    parent_dir = "./static/"+dir
    path = os.path.join(parent_dir, id) 
    os.mkdir(path) 
    for image in request.files.getlist("images"):
        path1 = os.path.join(path, image.filename) 
        image.save(path1) 
    f = request.files['file'] 
    path2 = os.path.join(path, "index.txt") 
    data=""
    for line in f.readlines():
        data +=  line.strip().decode("utf-8")
    with open( path2  ,'w') as fl:
        data=data.replace('src="','src="./static/'+dir+'/'+id+'/')
        fl.write(data)
    db = sqlite3.connect('web_data.db')
    title = request.form.get('title') 
    desciption = request.form.get('desciption')

    db.execute("INSERT INTO "+dir+" (id,title,desciption) VALUES ((?),(?),(?)) ",(id, title , desciption))
    db.commit()
    return redirect('/admin_control')
@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin_control', methods = ['GET'])
@login_required
def admin_control():
    return render_template("admin_control.html")

@app.route('/cultures')
@app.route('/articles')
def culture():
    db = sqlite3.connect('web_data.db')
    cursor = db.execute("SELECT * FROM +"+request.path[1:]+" ORDER BY date DESC LIMIT 10")
    rows = cursor.fetchall()
    return render_template("articles.html",rows=rows,dir=request.path)

########################################### done 



@app.route('/photography')
def photography():

    return render_template("mystories.html")

@app.route('/<page>',methods = ['GET']) 
@app.route('/<page>/<id>',methods = ['GET']) 
def page(page,id="empty"): 
    if page in ['cultures','articles'] and id!="empty":
        parent_dir = "./static/"+page
        path = os.path.join(parent_dir, id) 
        path = os.path.join(path, "index.txt") 
        data=""
        with open( path  ,'r') as f:
            for line in f.readlines():
                data +=  line.strip().decode("utf-8")
        return render_template(page[:-1]+".html",data=data)
    else:
        return render_template("error.html", top=403, bottom="page don't exist",url=request.path),403 
if __name__ == '__main__':
   app.run(host='0.0.0.0',port = "5000")

