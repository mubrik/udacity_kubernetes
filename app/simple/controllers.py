'''
  holds routes for simple app
'''
from os import environ as env
from typing import Dict
from flask import Blueprint, request, jsonify, abort
import jwt
from dotenv import load_dotenv
from .utils import requires_authentication

# load env
load_dotenv()

# get env vars
# for some reason aws isnt getting the JWT secret even tho it is in param store of region
# adding a default server side secret
JWT_SECRET = env.get('JWT_SECRET', "thisismysecret")
LOG_LEVEL = env.get('LOG_LEVEL', 'INFO')

simple_bp = Blueprint('simple_bp', __name__)

@simple_bp.route('/')
def index():
  return jsonify("Healthy")


@simple_bp.route('/auth', methods=['POST'])
def auth():
  data: None|Dict[str,str] = request.get_json()
  
  if data is None:
    abort(400, "No data provided")
    
  email = data['email']
  password = data['password']

  # check variabkes
  if email is None or password is None:
    return jsonify({'error': 'Data is incomplete'}), 400
  
  if JWT_SECRET is None:
    return jsonify({'error': 'Missing JWT'}), 400
  
  # create jwt token
  encoded_jwt = jwt.encode({'email': email, 'password': password}, JWT_SECRET, algorithm='HS256')
  
  return jsonify({'token': encoded_jwt.decode('utf-8')})


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
  

@simple_bp.errorhandler(422)
def handle_422(error):
  # bad syntax
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 422
  }), 422


@simple_bp.errorhandler(404)
def handle_404(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Resource not Found",
      "error": 404
  }), 404
  
@simple_bp.errorhandler(400)
def handle_400(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Bad Syntax",
      "error": 400
  }), 400


@simple_bp.errorhandler(405)
def handle_405(error):
  # Method Not Allowed
  return jsonify({
      "success": False,
      "message": "Method not allowed",
      "error": 405
  }), 405


@simple_bp.errorhandler(503)
def handle_503(error):
  # Server cannot process the request
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "System Busy",
      "error": 503
  }), 503
  