from actor import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)


class MirrorsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    fullname = db.Column(db.String(60), nullable=False)
    host = db.Column(db.String(60), nullable=False)
    path = db.Column(db.String(100), nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    help = db.Column(db.String(100), default=None)
    comment = db.Column(db.String(10), default=None)
    status = db.Column(db.Integer, nullable=False, default=0)   # 0 - active, 1 - muted
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(), onupdate=datetime.now())

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
    status = db.Column(db.Integer, nullable=False, default=0)   # 0 - active, 1 - muted
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(), onupdate=datetime.now())

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
        self.version = version

        if dir_info:
            self.dir = dir_info

        if path:
            self.path = path

        if comment:
            self.comment = comment


class MirrorsNotices(db.Model):
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)    # 0 - active, 1 - muted
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(), onupdate=datetime.now())

    def __init__(self, content, level="normal", created=None):
        self.content = content
        self.level = level

        if created is not None:
            self.created = created
