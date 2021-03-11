from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user and post."""
        
        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()
        db.session.commit()

        user = User(first_name="TestFirst", last_name="TestLast", img_url="https://picsum.photos/200/300")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="This title is a test", content="Content for testing")
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

        tag = Tag(name="TestTag")
        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

        post_tag = PostTag(post_id=f"{self.post_id}", tag_id=f"{self.tag_id}" )
        db.session.add(post_tag)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction"""

        db.session.rollback()
    
        

    
    def test_list_user(self):
        """Test whether users appear on user list"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)


    def test_show_user(self):
        with app.test_client() as client:
            """Test whether user page is created"""
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestFirst TestLast</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            """Test whether user is added to user list and HTML is displayed"""
            d = {"first name": "NewFirst", "last name": "NewLast", "img url": "https://picsum.photos/200/300"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('NewFirst NewLast', html)

    def test_edit_user(self):
        with app.test_client() as client:
            """Test whether a user can be edited"""
            d = {"first name": "EditFirst", "last name": "NewLast", "img url": "https://picsum.photos/200/300"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('EditFirst', html)
            self.assertNotIn('TestFirst', html)

    
   
    def test_delete_user(self):
        with app.test_client() as client:
            """Test whether user is deleted"""
           
            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('TestFirst', html)

      
    def test_add_post(self):
        with app.test_client() as client:
            """Test whether post is added and HTML is displayed"""
            d = {"title": "TestPost", "content": "Test Content"}
            resp = client.post(f"/users/1/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPost', html)
    
# This is failing.  response code 404 and the traceback states fully Null primary key identity cannot load any object.  Unsure exactly what the problem is, other tests on other objects using same format work with no issue.
    def test_edit_post(self):
        with app.test_client() as client:
            """Test whether a post can be edited"""
            d = {"title": "TestPost", "content": "Test Content"}
            
            resp = client.post(f"/posts/{self.post_id}/edit", data=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('EditPost', html)
            self.assertNotIn('This title', html)

   
    def test_delete_post(self):
        with app.test_client() as client:
            """Test whether post is deleted"""
            
            resp = client.post(f"/posts/{self.post_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('Content for testing', html)

    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTag', html)

    def test_add_tag(self):
        with app.test_client() as client:
            """Test whether tag is added and HTML is displayed"""
            d = {"name": "TempTag"}
            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TempTag', html)
    
    def test_edit_tag(self):
        with app.test_client() as client:
            """Test whether a tag can be edited"""
            d = {"name": "EditTag"}
            resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('EditTag', html)
            self.assertNotIn('TestTag', html)
    
    def test_delete_tag(self):
        with app.test_client() as client:
            """Test whether tag is deleted"""

            resp = client.post(f"/tags/{self.tag_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('TestTag', html)
