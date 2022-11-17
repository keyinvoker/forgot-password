from flask import request
from flask_restful import Resource

from app.schemas import LoginSchema

class Login(Resource):
    def post(self):
        data = request.form
        name = data['name']
        email = data['email']
        password = data['password']

        err = LoginSchema().validate(data)
        if err:
            return err