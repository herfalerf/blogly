from unittest import TestCase

from app import app
from models import db, User, Post

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
        
        Post.query.delete()
        User.query.delete()
        db.session.commit()

      
      
        user = User(first_name="TestFirst", last_name="TestLast", img_url="https://picsum.photos/200/300")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="This title is a test", content="Content for testing")
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

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
            d = {"first name": "NewFirst", "last name": "NewLast", "img url": "https://picsum.photos/200/300"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('NewFirst NewLast', html)
    
   

    def test_delete_user(self):
        with app.test_client() as client:
           
            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('TestFirst', html)

      


    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "TestPost", "content": "Test Content"}
            resp = client.post(f"/users/1/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPost', html)

   

            
