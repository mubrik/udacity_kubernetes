'''
  init file, set up the app
'''
from os import environ as env
from flask import Flask
from logging import Formatter, FileHandler, StreamHandler

from dotenv import load_dotenv

# load env
load_dotenv()

# get env vars
LOG_LEVEL = env.get('LOG_LEVEL', 'INFO')

# define WSGI app
app = Flask(__name__)

# Import a module / component using its blueprint handler variable
from .simple.controllers import simple_bp as simple_blueprint

# Register blueprint(s)
app.register_blueprint(simple_blueprint)

#  logging
if not app.debug:
  stream_handler = StreamHandler()
  stream_handler.setFormatter(
    Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  )
  app.logger.setLevel(LOG_LEVEL)
  stream_handler.setLevel(LOG_LEVEL)
  app.logger.addHandler(stream_handler)
  app.logger.debug(f'Starting with log level: {LOG_LEVEL}')

