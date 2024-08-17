from . import db

class SessionDB(db.Model):
    token        = db.Column(db.String(64), primary_key=True)
    problem_num  = db.Column(db.Integer)
    life         = db.Column(db.Integer)
    description  = db.Column(db.Text)
    option1      = db.Column(db.Text)
    option2      = db.Column(db.Text)
    option3      = db.Column(db.Text)
    option4      = db.Column(db.Text)
    result1      = db.Column(db.Integer)
    result2      = db.Column(db.Integer)
    result3      = db.Column(db.Integer)
    result4      = db.Column(db.Integer)
    result_text  = db.Column(db.Text)
    conv_archive = db.Column(db.Text)
    image_num    = db.Column(db.Integer)