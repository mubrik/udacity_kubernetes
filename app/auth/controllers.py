'''
  holds the blueprint routes for auth
'''
from flask import Blueprint,request, jsonify, make_response
from .models import User

# auth bp
auth_bp = Blueprint('auth', __name__)

@auth_bp.after_request
def after(response):
  # add to headers after controllers
  response.headers.add('Access-Control-Allow-Headers',
                       'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods',
                       'GET,PATCH,POST,DELETE,OPTIONS')
  return response

@auth_bp.route('/test')
def test():
  # test
  return jsonify({'message': 'test'})