from flask import request, session
from flask_login import login_user
from flask.ext.restful import Api
from flask_login import LoginManager, login_required
from irianas_server.api import (User)
from irianas_server.user import AuthSSH, User as UserLogin
user = None


def build_app(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return user

    @app.route('/login/form', methods=['POST'])
    def login():
        if request.form.get('username') and request.form.get('password'):
            result = AuthSSH.login(request.form.get('username'),
                                   request.form.get('password'))
            if result:
                user = UserLogin(request.form.get('username'), 1)
                login_user(user)
                session['login'] = 'aaa'
                return "1"
            else:
                return "0"
        else:
            return "100"

    @app.route('/u')
    @login_required
    def u():
        return "Hola"

    @app.route('/i')
    def i():
        return session['login']

    api = Api(app)

    #api.add_resource(Login, '/login')
    #api.add_resource(User, '/user/<string:username>', '/user')
