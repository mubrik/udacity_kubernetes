'''
  Models for post
'''
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  '''
    base class for inheritance of id and dates
  '''
  __abstract__  = True

  id = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                          onupdate=db.func.current_timestamp())


class Post(Base):
  '''
    Post Model
  '''
  __tablename__ = 'posts'

  title = db.Column(db.String(128), nullable=False)
  content = db.Column(db.String(500), nullable=False)

  def __init__(self, title, content):
    self.title = title
    self.email = content

  def __repr__(self):
    return f'<Post id:{self.id} title:{self.title}>'