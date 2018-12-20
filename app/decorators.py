from flask import request, jsonify


def login_required(f):
    def verify(*args, **kwargs):
        auth = request.headers.get('Authorization', '').split()
        if auth.length != 2:
            return jsonify({'message': '您发送的token格式有误'})
        return '123'
    return verify