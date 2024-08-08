from flask import redirect, render_template, session
def apology(message, code=400):

    return render_template("apology.html", top=code, bottom=message), code