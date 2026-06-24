from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import decode_jwt

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Authorization header is missing'}), 401

        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({'message': 'Authorization header must be Bearer token'}), 401

        token = parts[1]
        payload = decode_jwt(token)

        if isinstance(payload, str):
            # Error message was returned
            return jsonify({'message': payload}), 401

        # Add the decoded payload to request context so route functions can use it
        request.user = payload
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        if request.user.get('role') != 'ADMIN':
            return jsonify({'success': False, 'message': '관리자 권한이 필요합니다.'}), 403
        return f(*args, **kwargs)
    return decorated_function
