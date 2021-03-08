"""Seed files to make sample data for db"""

from models import User, Post, db 
from app import app

db.drop_all()
db.create_all()

joe = User(first_name="Joe", last_name="Blow", img_url="https://picsum.photos/200/300")
bill = User(first_name="Bill", last_name="Yardbird", img_url="https://picsum.photos/200/300")
janet = User(first_name="Janet", last_name="Jetplane", img_url="https://picsum.photos/200/300")
catdog = User(first_name="Cat", last_name="Dog", img_url="https://picsum.photos/200/300")
bjorn = User(first_name="Bjorn", last_name="Bjornson", img_url="https://picsum.photos/200/300")

p1 = Post(title="Post1", content="This is a test, this is only a test", user_id=1)
p2 = Post(title="Post2", content="This is a test, this is only a test", user_id=1)
p3 = Post(title="Post3", content="This is a test, this is only a test", user_id=1)
p4 = Post(title="Post4", content="This is a test, this is only a test", user_id=2)
p5 = Post(title="Post5", content="This is a test, this is only a test", user_id=2)

db.session.add_all([joe, bill, janet, catdog, bjorn])

db.session.commit()

db.session.add_all([p1,p2,p3,p4,p5])

db.session.commit()