'''
  holds test cases for the auth module
'''
import unittest
from app import app, db

class PostTestCase(unittest.TestCase):
  '''
    base class for auth tests
  '''
  def setUp(self):
    '''
      set up
      Define test variables and initialize app.
    '''
    app.testing = True
    self.app = app
    self.client = self.app.test_client
    # binds the app to the current context
    with self.app.app_context():
      self.db = db 
      # create all tables
      self.db.create_all()
    pass


  def tearDown(self):
    '''
      tear down
    '''
    pass
  
  
  def test_something(self):
    '''
      test something
    '''
    result = self.client().get('/api/post/test')
    self.assertEqual(result.status_code, 200)
    self.assertIn('post', result.json['message'])
    pass