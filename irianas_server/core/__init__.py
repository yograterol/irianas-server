from flask.ext.restful import Api
from irianas_server.api import LoginAPI, UserAPI, ClientAPI


def build_app(app):
    api = Api(app)
    api.add_resource(LoginAPI, '/login/<string:user>', '/login')
    api.add_resource(UserAPI, '/user/<string:action>', '/user')
    api.add_resource(ClientAPI, '/client/<string:action>', '/client')
