'''
  holds auth functions and decorator
'''
from flask import abort, request
from functools import wraps

def get_token_auth_header():
  '''
    gets the token from the header
  '''
  if 'Authorization' not in request.headers:
    raise abort(401, 'Authorization header is expected.')
  # get Auth header  
  auth_header = request.headers['Authorization']
  # split header
  split_auth_header = auth_header.split(' ')
  # checks validity of header
  if len(split_auth_header) != 2:
    raise abort(401, 'Invalid authorization header')
  elif split_auth_header[0] != 'Bearer':
    raise abort(401, 'Invalid bearer header')
  return split_auth_header[1]


def requires_authentication(func):
  '''
    requires auth, user has to be authenticated and has to have the permission
  '''
  @wraps(func)
  def wrapper(*args, **kwargs):
    print(*args, **kwargs)
    #  will raise exception f errors
    token = get_token_auth_header()
    return func(token)
  return wrapper
