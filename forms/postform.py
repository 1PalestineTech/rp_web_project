from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

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