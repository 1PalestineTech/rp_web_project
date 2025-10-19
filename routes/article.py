from flask import Blueprint, render_template

article_bp = Blueprint('article', __name__)


@article_bp.route('/articles')
def articles():
    return render_template("articles.html",title="Articles",
                           message="At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum")