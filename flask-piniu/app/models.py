from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
#    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    is_index = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref="parent", lazy='dynamic',
                            cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<Page: id=%r, title=%s, is_index=%s'\
                % (self.id, self.title, self.is_index)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    data = db.Column(db.String(140), unique=False)
    images = db.Column(db.String(140), unique=False)
    attachments = db.Column(db.String(140), unique=False)
    contact = db.Column(db.Boolean, default=False) #is it contact form?
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    background = db.Column(db.String(140), unique=False) ###### HERE

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))

    def __repr__(self):
        return '<Post: id=%r, contact=%s, background=%s'\
                % (self.id, self.contact, self.background)


class Sortable(db.Model):
    __tablename__ = "sortables"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=True)
    data = db.Column(db.String(140), unique=False)

    def __repr__(self):
        return '<Sortable: id=%r, data=%s'\
                % (self.id, self.data)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    numer = db.Column(db.String(70), unique=False)
    miejsce = db.Column(db.String(70), unique=False)
    opis = db.Column(db.String(70), unique=False)
    data = db.Column(db.String(70), unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    reminder = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Order: id=%r, timestamp=%s, reminder=%s'\
                % (self.id, self.timestamp, self.reminder)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
