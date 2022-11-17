from app.resources.login import Login
from app.resources.forgot_password import ForgotPassword
from app import api

api.add_resource(Login, '/login')
api.add_resource(ForgotPassword, '/forgot-password')