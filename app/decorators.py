from flask import request, jsonify, current_app
from app.models.User import User
import jwt


def login_required(f):
    def verify(*args, **kwargs):
        auth = request.headers.get('Authorization', '').split()
        if len(auth) != 2:
            return jsonify({'message': '您发送的token格式有误'})
        try:
            token = auth[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['user']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token失效'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'token无效'}), 401

    return verify
