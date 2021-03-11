"""Seed files to make sample data for db"""

from models import User, Post, db, Tag, PostTag
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

t1 = Tag(name="Fun")
t2 = Tag(name="Exciting")
t3 = Tag(name="Cats")
t4 = Tag(name="Garbage")
t5 = Tag(name="Propaganda")

pt1 = PostTag(post_id="1", tag_id="1")
pt2 = PostTag(post_id="1", tag_id="3")
pt3 = PostTag(post_id="2", tag_id="4")
pt4 = PostTag(post_id="2", tag_id="5")
pt5 = PostTag(post_id="3", tag_id="2")
pt6 = PostTag(post_id="4", tag_id="3")
pt7 = PostTag(post_id="4", tag_id="5")
pt8 = PostTag(post_id="5", tag_id="1")
pt9 = PostTag(post_id="5", tag_id="4")

db.session.add_all([joe, bill, janet, catdog, bjorn])

db.session.commit()

db.session.add_all([p1,p2,p3,p4,p5])

db.session.commit()

db.session.add_all([t1,t2,t3,t4,t5])

db.session.commit()

db.session.add_all([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9])

db.session.commit()
