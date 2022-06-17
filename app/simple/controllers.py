'''
  holds routes for simple app
'''
from os import abort, environ as env
from flask import Blueprint, request, jsonify
import jwt
from dotenv import load_dotenv
from .utils import requires_authentication

# load env
load_dotenv()

# get env vars
JWT_SECRET = env.get('JWT_SECRET', None)
LOG_LEVEL = env.get('LOG_LEVEL', 'INFO')

simple_bp = Blueprint('simple_bp', __name__)

@simple_bp.route('/')
def index():
  return "Healthy"


@simple_bp.route('/auth', methods=['POST'])
def auth():
  data = request.get_json()
  email = data['email']
  password = data['password']
  print(email, password)
  # check variabkes
  if email is None or password is None:
    return jsonify({'error': 'No data'}), 400
  
  if JWT_SECRET is None:
    return jsonify({'error': 'Missing JWT'}), 400
  
  # create jwt token
  encoded_jwt = jwt.encode({'email': email, 'password': password}, JWT_SECRET, algorithm='HS256')
  
  return encoded_jwt


@simple_bp.route('/contents')
@requires_authentication
def get_payload(token):
  print(token)
  
  # decoe token
  try:
    decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
  except jwt.exceptions.DecodeError:
    return jsonify({'error': 'Not enough segments in Auth header'}), 401

  
  return jsonify(decoded)
  