from flask import request, render_template, session
from models import db
from functools import wraps
from models.Writers import Writer
from models.Admins import Admin


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = db.session.query(Admin).filter_by(id=session.get("user_id")).first()
        if not admin:
            return render_template("error.html", top=403, bottom="No Permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        writer = db.session.query(Writer).filter_by(id=session.get("user_id")).first()
        if not writer:
            return render_template("error.html", top=403, bottom="No Permission",url=request.path),403 
        return f(*args, **kwargs)

    return decorated_function


