'''
  holds the blueprint routes for user
'''
from flask import Blueprint, jsonify
from .models import User

# user bp
user_bp = Blueprint('user', __name__)

@user_bp.route('/test')
def test():
  # test
  return jsonify({'message': 'test'})