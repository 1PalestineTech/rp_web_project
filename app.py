from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask_session import Session
import re, sqlite3, shortuuid, os.path, os, shutil
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils import admin_writter_required, admin, admin_writter_editor_required

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['CKEDITOR_ENABLE_CSRF'] = True  
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')
app.secret_key = 'soifaoijfaqd4894'
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)

class PostForm(FlaskForm):
    title = StringField('Title')
    db = sqlite3.connect('web_data.db')
    cursor = db.execute("SELECT * FROM Tags")
    rows = cursor.fetchall()
    tg = list (map(lambda e: (e[0], e[1]),rows))
    tags = SelectField('Tags', choices = tg)
    desciption = TextAreaField('Desciption')
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()
class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField()




#                                        LOGIN
@app.route('/login', methods = ['GET','POST'])
def login():
    form=Login()
    db = sqlite3.connect('web_data.db')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cursor = db.execute("SELECT * FROM Users WHERE username = (?) ",(username,))
        rows = cursor.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2],password):
            return render_template("error.html", top=403, bottom="invalid username and/or password",url=request.path),403
        session["user_id"] = rows[0][0]
        return redirect("/")
    else :
        if not (session.get("user_id") is None):
            return redirect('/')
        else:
            return render_template("login.html",form=form)
        

#                                        LOGOUT
@app.route('/logout', methods = ['POST','GET'])
def logout():
    session.clear()
    return redirect('/')




#                                        CHANGE PASSWORD
@app.route('/change_password', methods = ['GET','POST'])
@admin_writter_editor_required
def change_password():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        if not request.form.get("old_password"):
            return render_template("error.html", top=403, bottom="must provide old password",url=request.path),403 

        elif not request.form.get("new_password"):
            return render_template("error.html", top=403, bottom="must provide the new password",url=request.path),403 
        old_password = request.form.get('old_password').strip()
        new_password = request.form.get('new_password').strip()
        cursor = db.execute("SELECT * FROM Users WHERE id = (?) ",(session.get("user_id"),))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][2],old_password):
            return render_template("error.html", top=403, bottom="wrong password",url=request.path),403
        hs=generate_password_hash(new_password) 
        db.execute("UPDATE Users SET password = (?) WHERE id = (?)",(hs,session.get("user_id")))
        db.commit()
        
        return redirect("/")
    else :
        return render_template("change_password.html")




#                                        ADD WRITER
@app.route('/add_writer', methods = ['GET','POST'])
@admin
def add_writer():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if not request.form.get("username"):
            return render_template("error.html", top=403, bottom="must provide username",url=request.path),403 

        elif not request.form.get("password"):
            return render_template("error.html", top=403, bottom="must provide password",url=request.path),403 
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM Users WHERE username = (?) ",(username,))
        rows = cursor.fetchall()
        if len(rows)>0:
            return render_template("error.html", top=403, bottom="username aleardy exist",url=request.path),403 
        id = shortuuid.ShortUUID().random(length=20)
        hs=generate_password_hash(password)
        db.execute("INSERT INTO Users (id,username,password) VALUES ((?),(?),(?)) ",(id, username, hs))
        db.execute("INSERT INTO Writters (id) VALUES (?) ",(id,))
        db.commit()
        return redirect('/remove_writer')
    else:
        return render_template("add_writer.html")





#                                        REMOVE Writter
@app.route('/remove_writer', methods = ['GET','POST'])
@admin
def remove_admin():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        
        ids = request.form.getlist('admins')
        for id in ids:
            cursor = db.execute("SELECT * FROM Admins WHERE id = (?) ",(id,))
            rows = cursor.fetchall()
            if len(rows)!=1:
                db.execute("DELETE FROM Writers WHERE id = (?) ",(id,))
                db.execute("DELETE FROM Users WHERE id = (?) ",(id,))
                
                db.commit()
        return redirect('/remove_writer')
    
    cursor = db.execute("SELECT * from Writers where id not in (select id from Admins) ")
    rows = cursor.fetchall()
    return render_template("remove_writer.html",admins=rows)

#                                        ADD EDITOR
@app.route('/add_editor', methods = ['GET','POST'])
@admin
def add_editor():
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if not request.form.get("username"):
            return render_template("error.html", top=403, bottom="must provide username",url=request.path),403 

        elif not request.form.get("password"):
            return render_template("error.html", top=403, bottom="must provide password",url=request.path),403 
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM Users WHERE username = (?) ",(username,))
        rows = cursor.fetchall()
        if len(rows)>0:
            return render_template("error.html", top=403, bottom="username aleardy exist",url=request.path),403 
        id = shortuuid.ShortUUID().random(length=20)
        hs=generate_password_hash(password)
        db.execute("INSERT INTO Users (id,username,password) VALUES ((?),(?),(?)) ",(id, username, hs))
        db.execute("INSERT INTO Editors (id) VALUES (?) ",(id,))
        db.commit()
        return redirect('/remove_editor')
    else:
        return render_template("add_writer.html")




#                                        REMOVE EDITOR
@app.route('/remove_editor', methods = ['GET','POST'])
@admin
def remove_editor():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        
        ids = request.form.getlist('admins')
        for id in ids:
            cursor = db.execute("SELECT * FROM Admins WHERE id = (?) ",(id,))
            rows = cursor.fetchall()
            if len(rows)!=1:
                db.execute("DELETE FROM Editors WHERE id = (?) ",(id,))
                db.execute("DELETE FROM Users WHERE id = (?) ",(id,))
                
                db.commit()
        return redirect('/remove_editor')
    
    cursor = db.execute("SELECT * from Editors where id not in (select id from Admins) ")
    rows = cursor.fetchall()
    return render_template("remove_writer.html",admins=rows)






#                                        ADD Article
@app.route('/post', methods=['GET', 'POST'])
@admin_writter_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        tag= form.tags.data
        id = str(shortuuid.ShortUUID(alphabet="013456789").random(length=20))
        parent_dir = "./static/articles"
        path = os.path.join(parent_dir, id) 
        os.mkdir(path) 
        path2 = os.path.join(path, "index.txt") 
        with open( path2  ,'w') as fl:
            fl.write(body)
        db = sqlite3.connect('web_data.db')
        title = form.title.data
        desciption = form.desciption.data

        db.execute("INSERT INTO Articles (id,title,desciption) VALUES ((?),(?),(?)) ",(id, title , desciption))
        db.execute("INSERT INTO Categorize (article_id,tag_id) VALUES ((?),(?)) ",(id, tag))
        db.execute("INSERT INTO Actions (article_id,user_id,type) VALUES ((?),(?),(?)) ",(id, session.get("user_id") , "write"))
        db.commit()
        return redirect('/article/'+id)
    else:
         return render_template("post.html",form=form)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    file_name = shortuuid.ShortUUID().random(length=20) + "." + extension
    f.save(os.path.join(app.config['UPLOADED_PATH'], file_name))
    url = url_for('uploaded_files', filename=file_name)
    return upload_success(url, filename=file_name)

@app.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


#                                        EDIT ARTICLE
@app.route('/edit/<id>', methods = ['GET','POST'])
@admin_writter_editor_required
def edit(id):
    form = PostForm()
    parent_dir = "./static/articles"
    path = os.path.join(parent_dir, id) 
    path = os.path.join(path, "index.txt")
    db = sqlite3.connect('web_data.db')
    if form.validate_on_submit():
       tag = form.tags.data
       with open( path  ,'w') as fl:
            fl.write(form.body.data)
       db.execute("INSERT INTO Actions (article_id,user_id,type) VALUES ((?),(?),(?)) ",(id, session.get("user_id") , "edit"))
       db.execute("DELETE FROM Categorize WEHRE article_id = (?) ",(id, ))
       db.execute("INSERT INTO Categorize (article_id,tag_id) VALUES ((?),(?)) ",(id, tag))
       db.commit()
       return redirect('/article/'+id)
    elif id != "empty":
        cursor = db.execute("SELECT * FROM Articles WHERE id =?",(id,))
        rows = cursor.fetchall()
        data=""
        if len(rows)>0:
            with open( path  ,'r') as f:
                for line in f.readlines():
                    data +=  line.strip()
            
            form.title.data = rows[0][1]
            form.desciption.data = rows[0][2]
            form.tags.data = "aaaa"
            form.body.data = data
            return render_template("edit_post.html",form=form)
        return render_template("error.html", top=403, bottom="page don't exist",url=request.path),403 
    else:
        return render_template("error.html", top=403, bottom="page don't exist",url=request.path),403 
    
    


#                                        REMOVE Article
@app.route('/remove/<id>', methods = ['GET','POST'])
@admin_writter_required
def remove(id):
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        parent_dir = "./static/articles"
        path = os.path.join(parent_dir, id)     
        shutil.rmtree(path)
        db.execute("DELETE FROM Articles WHERE id = (?) ",(id,))
        db.execute("DELETE FROM Categorize WHERE article_id = (?) ",(id,))
        db.execute("INSERT INTO Actions (article_id,user_id,type) VALUES ((?),(?),(?)) ",(id, session.get("user_id") , "delete"))
        db.commit()
        path = os.path.join(path, "index.txt") 
        return redirect('/articles')
    return 


#                                        HOME PAGE (Fixed)
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")



#                                      ABOUT US (Fixed)
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/timeline')
def timeline():
    return render_template("timeline.html")






#                                        ARTICLES PAGE

@app.route('/articles')
def articles():
    db = sqlite3.connect('web_data.db')
    print(request.path[1:])
    cursor = db.execute("SELECT * FROM Articles ORDER BY date DESC")
    rows = cursor.fetchall()
    return render_template("articles.html",rows=rows)







#                                        LOAD ARTICLES
@app.route('/article/<id>',methods = ['GET']) 
def page(id="empty"): 
    if id != "empty":
        parent_dir = "./static/articles"
        path = os.path.join(parent_dir, id) 
        path = os.path.join(path, "index.txt") 
        data=""
        with open( path  ,'r') as f:
            for line in f.readlines():
                data +=  line.strip()
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT title FROM Articles WHERE id =?",(id,))
        rows = cursor.fetchall()
        title=rows[0][0]
        return render_template("page.html",title=title,data=data)
    else:
        return render_template("error.html", top=403, bottom="page don't exist",url=request.path),403 
    



if __name__ == "__main__":
   app.run(host='0.0.0.0')
