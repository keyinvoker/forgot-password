from flask import request
from flask_restful import Resource

from app.models.user import User

class ForgotPassword(Resource):
    def post(self):
        # submit form:
        #    - email (filled in automatically if using UI) or ID
        #    - password

        id = 1 # TODO: get dynamically
        password = request.form['password']
        user = User.query.filter_by(id=id).first()

        # validate:
        #    - if same with old password, reject
        #    - if no at least one caps, one number & one symbol, reject

        # x

        # update password
        user.password = password
        user.update()
        return