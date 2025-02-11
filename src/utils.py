from flask import request, render_template, session
import sqlite3
from functools import wraps

def admin_writter_editor_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = sqlite3.connect('web_data.db')
        
        if session.get("user_id") is None :
            return render_template("error.html", top=503, bottom="no permission",url=request.path),503
        
        cursor = db.execute("""
                SELECT * FROM Editors FULL JOIN Admins 
                ON Admins.id = Editors.id FULL JOIN Writters
                ON Admins.id = Writters.id
                            
                WHERE Admins.id = (?) OR Writters.id = (?) OR Editors.id = (?)"""  
                ,(session.get("user_id"),session.get("user_id"),session.get("user_id")))
        rows = cursor.fetchall()
        if len(rows) !=1 :
            return render_template("error.html", top=403, bottom="no permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function



def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("SELECT * FROM Admins WHERE id = (?) ",(session.get("user_id"),))
        rows = cursor.fetchall()
        if len(rows) !=1 :
            return render_template("error.html", top=403, bottom="no permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function
def admin_writter_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = sqlite3.connect('web_data.db')
        cursor = db.execute("""
                SELECT * FROM Admins FULL JOIN Writters
                ON Admins.id = Writters.id
                WHERE Admins.id = (?) OR Writters.id = (?) """  
                ,(session.get("user_id"),session.get("user_id")))
        rows = cursor.fetchall()
        if len(rows) !=1 :
            return render_template("error.html", top=403, bottom="no permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function


