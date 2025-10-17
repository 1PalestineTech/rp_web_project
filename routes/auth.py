from flask import Blueprint, request
from forms.authforms.py import Login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['GET','POST'])
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