from flask import request, render_template, session
import sqlite3
from functools import wraps

def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM Admins WHERE id = (?) ",(session.get("user_id"),))
        rows = cursor.fetchall()
        if len(rows) !=1 :
            return render_template("error.html", top=403, bottom="No Permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM Users WHERE id = (?)",(session.get("user_id"),))
        rows = cursor.fetchall()
        if len(rows) !=1 :
            return render_template("error.html", top=403, bottom="No Permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function


