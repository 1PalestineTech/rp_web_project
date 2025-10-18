from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
@main_bp.route('/index')
def index():
    return render_template("index.html")

@main_bp.route('/about')
def about():
    return render_template("about.html",
                           title="About Us",
                           message="At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum")