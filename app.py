from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory,jsonify
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import StringField, SubmitField, SelectField, TextAreaField,HiddenField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success
from flask_session import Session
import re, sqlite3, shortuuid, os.path, os, shutil
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils import login_required, admin

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
    tags = SelectField('Tags', choices=[])  # Set default empty
    tags_values = HiddenField("tags_values")
    desciption = TextAreaField('Desciption')
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        try:
            db = sqlite3.connect(os.path.join(basedir, 'web_data.db'))
            cursor = db.execute("SELECT * FROM Tags")
            rows = cursor.fetchall()
            self.tags.choices = [(row[0], row[1]) for row in rows]
        except Exception as e:
            self.tags.choices = []
            # optionally log e
class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField()

class Delete(FlaskForm):
    pass


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
            return render_template("error.html", top=403, bottom="Invalid Username And/Or Password",url=request.path),403
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
@login_required
def change_password():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        if not request.form.get("old_password"):
            return render_template("error.html", top=403, bottom="Must Provide Old Password",url=request.path),403 

        elif not request.form.get("new_password"):
            return render_template("error.html", top=403, bottom="Must Provide The New Password",url=request.path),403 
        old_password = request.form.get('old_password').strip()
        new_password = request.form.get('new_password').strip()
        cursor = db.execute("SELECT * FROM Users WHERE id = (?) ",(session.get("user_id"),))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][2],old_password):
            return render_template("error.html", top=403, bottom="Wrong Password",url=request.path),403
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
            return render_template("error.html", top=403, bottom="Must Provide Username",url=request.path),403 

        elif not request.form.get("password"):
            return render_template("error.html", top=403, bottom="Must Provide Password",url=request.path),403 
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM Users WHERE username = (?) ",(username,))
        rows = cursor.fetchall()
        if len(rows)>0:
            return render_template("error.html", top=403, bottom="Username Aleardy Exist",url=request.path),403 
        id = shortuuid.ShortUUID().random(length=20)
        hs=generate_password_hash(password)
        db.execute("INSERT INTO Users (id,username,password) VALUES ((?),(?),(?)) ",(id, username, hs))
        db.execute("INSERT INTO Writters (id) VALUES (?) ",(id,))
        db.commit()
        return redirect('/remove_writer')
    else:
        return render_template("add_writer.html",form=Delete())





#                                        REMOVE Writter
@app.route('/remove_writer', methods = ['GET','POST'])
@admin
def remove_admin():
    db = sqlite3.connect('web_data.db')
    if request.method == "POST":
        
        ids = request.form.getlist('writters')
        print(ids)
        for id in ids:
            cursor = db.execute("SELECT * FROM Writters WHERE id = (?) ",(id,))
            rows = cursor.fetchall()
            if len(rows)>0:
                db.execute("DELETE FROM Writters WHERE id = (?) ",(id,))
                db.execute("DELETE FROM Users WHERE id = (?) ",(id,))
                db.commit()
        return redirect('/remove_writer')
    
    cursor = db.execute("SELECT * FROM Users WHERE id NOT IN (SELECT id FROM Admins)")
    rows = cursor.fetchall()
    return render_template("remove_writer.html",admins=rows,form=Delete())


#                                        ADD Article
@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        tags_values = form.tags_values.data.split(",")
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
        for tag in tags_values:
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
@login_required
def edit(id):
    form = PostForm()
    parent_dir = "./static/articles"
    path = os.path.join(parent_dir, id) 
    path = os.path.join(path, "index.txt")
    db = sqlite3.connect('web_data.db')
    if form.validate_on_submit():
        with open( path  ,'w') as fl:
            fl.write(form.body.data)
        db.execute("DELETE FROM Categorize WHERE article_id = (?) ",(id, ))
        tags_values = form.tags_values.data.split(",")
        for tag in tags_values:
            db.execute("INSERT INTO Categorize (article_id,tag_id) VALUES ((?),(?)) ",(id, tag))
        db.execute("UPDATE Articles SET desciption = (?), title = (?) WHERE id =(?)",(form.desciption.data,form.title.data,id))
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
            form.body.data = data
            return render_template("edit_post.html",form=form)
        return render_template("error.html", top=403, bottom="Page Don't Exist",url=request.path),403 
    else:
        return render_template("error.html", top=403, bottom="Page Don't Exist",url=request.path),403 
    
    


#                                        DELETE Article
@app.route('/delete/<id>', methods = ['GET','POST'])
@login_required
def remove(id):
    db = sqlite3.connect('web_data.db')
    if request.method == "GET":
        parent_dir = "./static/articles"
        path = os.path.join(parent_dir, id)     
        shutil.rmtree(path)
        db.execute("DELETE FROM Articles WHERE id = (?) ",(id,))
        db.execute("DELETE FROM Categorize WHERE article_id = (?) ",(id,))
        db.execute("INSERT INTO Actions (article_id,user_id,type) VALUES ((?),(?),(?)) ",(id, session.get("user_id") , "delete"))
        db.commit()
        return "200"
    return "Done"


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
@app.route('/timeline/<id>')
def timeline_item(id):
    return render_template("timeline_item.html",id=id)





#                                        ARTICLES PAGE

@app.route('/articles')
def articles():
    form = Delete()
    db = sqlite3.connect('web_data.db')
    
    cursor = db.execute("SELECT * FROM Articles ORDER BY date DESC")
    rows = cursor.fetchall()
    cursor = db.execute("SELECT * FROM Tags ")
    tags = cursor.fetchall()
    return render_template("articles.html",rows=rows,user=session.get("user_id"),form=form,tags=tags)

#                                      Filter
@app.route('/filter',methods = ["POST","GET"])
def filter():
    db = sqlite3.connect('web_data.db')
    form = request.get_json()
    ids = form['tags'].strip()
    name = form['name'].strip()
    if len(ids) != 0 and not name.isalnum():
        cursor = db.execute(f"SELECT * FROM Articles WHERE id IN (SELECT article_id FROM Categorize WHERE tag_id IN ({ids})) ORDER BY date DESC")
    elif (not name.isalnum()) and  len(ids) == 0:
        cursor = db.execute("SELECT * FROM Articles ORDER BY date DESC")
    elif name.isalnum() and len(ids) != 0:
        cursor = db.execute(f"SELECT * FROM Articles WHERE id IN (SELECT article_id FROM Categorize WHERE tag_id = ({ids})) AND title LIKE (?) ORDER BY date DESC",("%"+name+"%",))
    else:
        cursor = db.execute("SELECT * FROM Articles WHERE title LIKE (?) ORDER BY date DESC",("%"+name+"%",))
    rows = cursor.fetchall()
    return  jsonify({"data":rows,"admin":session.get("user_id")})
    





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
        return render_template("error.html", top=403, bottom="Page Don't Exist",url=request.path),403 
    



if __name__ == "__main__":
   app.run(host='0.0.0.0')
