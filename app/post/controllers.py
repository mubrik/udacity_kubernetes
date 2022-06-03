'''
  holds the blueprint routes for post
'''
from flask import Blueprint,request, jsonify, make_response
from .models import Post

# post bp
post_bp = Blueprint('post', __name__)

@post_bp.after_request
def after(response):
  # add to headers after controllers
  response.headers.add('Access-Control-Allow-Headers',
                       'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods',
                       'GET,PATCH,POST,DELETE,OPTIONS')
  return response

@post_bp.route('/test')
def test():
  # test
  return jsonify({'message': 'post'})