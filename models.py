from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""



class User(db.Model):

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<id={u.id} first name={u.first_name} last name={u.last_name} img url={u.img_url}>"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)

    first_name = db.Column(db.String(50), 
                           nullable=False)

    last_name = db.Column(db.String(50), 
                          nullable=False)

    img_url = db.Column(db.String(2083), nullable=True)
    