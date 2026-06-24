import jwt
import datetime
from config import Config

def encode_jwt(user_id, email, role):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'email': email,
        'role': role
    }
    return jwt.encode(
        payload,
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )

def decode_jwt(auth_token):
    try:
        payload = jwt.decode(auth_token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
