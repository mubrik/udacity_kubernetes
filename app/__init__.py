'''
  init file, set up the app
'''
import sys
import unittest
from os import environ as env
from typing import List
from unittest import TestCase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

# load env
load_dotenv()

# get env vars
RUN_MODE = env.get('FLASK_RUN_MODE', 'development')
DB_TYPE = env.get('DB_TYPE', 'sqlite')

# define WSGI app
app = Flask(__name__)

if RUN_MODE == 'development':
  # dev
  app.config.from_object('config')
elif RUN_MODE == 'testing':
  app.config.from_object('config_test')

# Define the database object
db = SQLAlchemy(app)
# setup migration
migrate = Migrate(app, db)
# setup cors
cors = CORS(app, resources={"r*/api/*": {"origins": "*"}})

# Import a module / component using its blueprint handler variable
from .user.controllers import user_bp as user_blueprint
from .post.controllers import post_bp as post_blueprint

# Register blueprint(s)
app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(post_blueprint, url_prefix='/api/post')

# import cli functons
from .utils import *

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

if RUN_MODE == 'testing':
  # import test cases
  from .user.tests import UserTestCase
  from .post.tests import PostTestCase
  test_list: List[TestCase] = [UserTestCase, PostTestCase]
  # run tests
  for test in test_list:
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=2).run(suite)
  # exit
  sys.exit("Test Done")
