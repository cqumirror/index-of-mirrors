from actor import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class MirrorsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    fullname = db.Column(db.String(60), nullable=False)
    host = db.Column(db.String(60), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    help = db.Column(db.String(100), default=None)
    comment = db.Column(db.String(10), default=None)

    def __init__(self, fullname, host, path, protocol, help_url=None, comment=None):
        fullname_f = fullname.lower()
        if ' ' in fullname_f:
            fullname_f = '-'.join(fullname_f.split(' '))
        self.name = fullname_f
        self.fullname = fullname
        self.host = host
        self.path = path
        self.protocol = protocol

        if help_url:
            self.help = help_url

        if comment:
            self.comment = comment


class MirrorsResources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    fullname = db.Column(db.String(60), nullable=False)
    host = db.Column(db.String(60), nullable=False)
    dir = db.Column(db.String(40), default=None)
    path = db.Column(db.String(100), default=None)
    type = db.Column(db.String(10), nullable=False)
    version = db.Column(db.String(40), nullable=False)
    comment = db.Column(db.String(10), default=None)
    protocol = db.Column(db.String(10), nullable=False)

    def __init__(self, fullname, host, type_info, version,
                 protocol, dir_info=None, path=None, comment=None):
        fullname_f = fullname.lower()
        if ' ' in fullname_f:
            fullname_f = '-'.join(fullname_f.split(' '))
        self.name = fullname_f
        self.fullname = fullname
        self.host = host
        self.protocol = protocol
        self.type = type_info

        if dir_info:
            self.dir = dir_info

        if path:
            self.path = path

        if comment:
            self.comment = comment
