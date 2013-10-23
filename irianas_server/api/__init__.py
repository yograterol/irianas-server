# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import datetime
import requests
from flask import request, session
from flask.ext.restful import Resource, abort
from irianas_server.user import AuthSSH
from irianas_server.user import ManageUserServer
from irianas_server.models import RecordSession, Client
from irianas_server.client import ManageClient, ClientBasicTask


def requires_ssl(f):
    def inner(*args, **kwargs):
        val = request.url
        if not val.startswith('https'):
            return dict(error='SSLError')
        return f(*args, **kwargs)
    return inner


def check_token(f):
    def inner(*args, **kwargs):
        time_min = datetime.datetime.now() - datetime.timedelta(0, 3600)
        time_now = datetime.datetime.now()
        if request.form.get('token'):
            ses = RecordSession.objects(token=request.form.get('token'),
                                        token_end__gte=time_min)
            if not ses:
                return abort(401)

            if time_now > ses[0].token_end:
                return abort(401)
            else:
                session['username'] = ses[0].user
                return f(*args, **kwargs)
        else:
            return abort(401)
    return inner


class LoginAPI(Resource):

    @check_token
    @requires_ssl
    def get(self):
        return dict(login=session['username'])

    @requires_ssl
    def post(self):
        return AuthSSH.login(request.form['user'], request.form['pass'])

    @check_token
    @requires_ssl
    def put(self, user):
        ses = RecordSession.objects(token=request.form.get('token'),
                                    user=user)
        if not ses:
            return abort(401)
        ses = ses[0]
        time = datetime.datetime.now() - datetime.timedelta(0, 3600)
        ses.token_end = time
        ses.save()
        return dict(action="Logout")

# Manage User REST API
# ****** BEGIN ******


class UserAPI(Resource):
    ma = ManageUserServer()
    method_decorators = [requires_ssl, check_token]

    def post(self):
        if self.ma.add_user(request.form['user'], request.form['pass']):
            return dict(user=request.form['user'],
                        action="Created")
        else:
            return dict(user=request.form['user'],
                        action="NotCreated")

    def put(self, action='Update'):
        if action == 'Update':
            if self.ma.update_user(request.form['user'], request.form['pass']):
                return dict(user=request.form['user'],
                            action="Updated")
            else:
                return dict(user=request.form['user'],
                            action="NotUpdated")
        else:
            if self.ma.delete_user(request.form['user']):
                return dict(user=request.form['user'],
                            action="Deleted")
            else:
                return dict(user=request.form['user'],
                            action="NotDeleted")

# ****** END ******

# Manage Clients REST API
# ****** BEGIN ******


class ClientAPI(Resource):
    method_decorators = [requires_ssl, check_token]

    def get(self, action='List'):
        result = None
        if action == 'List':
            clients = Client.objects
            if clients:
                result = list()
                for client in clients:
                    result.append(dict(ip=client.ip_address,
                                       services=client.services_install))
                return dict(result=result)
            else:
                return abort(404)
        else:
            client = Client.objects(ip_address=request.form['ip_address'])
            if client:
                client = client[0]
                return dict(ip_address=request.form['ip_address'],
                            services=client.services_install)
            return abort(404)

    def post(self):
        return ManageClient.connect_client()

    def put(self):
        return ManageClient.delete_client()


# ****** END ******

# Client Basic Tasks
class ClientBasicTaskAPI(Resource):

    method_decorators = [requires_ssl, check_token]

    def get(self, action):
        return ClientBasicTask.request_task(action)

# ****** END ******


class ClientServicesAPI(Resource):

    method_decorators = [requires_ssl, check_token]
    url = 'https://{ip}:9000/api/services/{service}/{action}'

    def get(self, services, action):
        r = requests.get(self.url)
        if r.status_code == 200:
            return r.json()
        else:
            return dict(error=0)

