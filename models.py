from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)

    first_name = db.Column(db.String(50), 
                           nullable=False)

    last_name = db.Column(db.String(50), 
                          nullable=False)

    img_url = db.Column(db.String(2083), nullable=True)

    def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last name={u.last_name} img url={u.img_url}>"

    

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(50),
                      nullable=False)
    
    content = db.Column(db.String(2083), 
                        nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}"

