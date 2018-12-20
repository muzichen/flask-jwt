from flask import jsonify, request, current_app
from datetime import datetime, timedelta
from app.models.User import User
from app.decorators import login_required
from app import db
from . import api

import jwt


@api.route('/register', methods=('POST',))
def register():
    data = request.get_json()
    user = User()
    user.email = data['email']
    user.password = data['password']
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@api.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(email=data['email'], password=data['password'])
    # 如果用户名或密码验证不通过，则直接返回错误信息
    if not user:
        return jsonify({'message': '用户名或密码错误'}), 401

    # 如果用户名和密码验证通过，则生成token
    token = jwt.encode({
        'aud': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, current_app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('utf-8')})


@api.route('/test/token', methods=('POST',))
@login_required
def test_token():
    return '123'
