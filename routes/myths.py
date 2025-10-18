from flask import Blueprint, render_template

myths_bp = Blueprint('myths', __name__)


@myths_bp.route('/myths')
def myths():
    return render_template("myths.html")