# util.py was added for module 13 lesson 3 implementing jwt
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from flask import request, jsonify
from functools import wraps

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def encode_token(user_id, role_names):
    payload ={
        'exp': datetime.now() + timedelta(days=1),
        'iat' :datetime.now(),
        'sub':user_id,
        'roles': role_names

    }
    token = jwt.encode(payload, SECRET_KEY,algorithm='HS256')
    return token

#adding for implementing access control
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
                print("Token:", token)
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print(payload['sub'])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired', 'error': 'Unauthorized'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token', 'error': 'Unauthorized'}), 401
        if not token:
            return jsonify({'message': 'Authorication Token is missing', 'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

# adding for role implentation
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return jsonify({'message': 'Authorication Token is missing'}), 401
                
            try: 
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
            
            roles = payload["roles"]

            if role not in roles:
                return jsonify({'message': 'User does not have the required role'}), 403
            return f(*args, **kwargs)
        
        return decorated_function

    return decorator    