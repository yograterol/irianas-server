# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import datetime
import requests
import platform
import psutil
import mongoengine
import socket
from copy import deepcopy
from functools import wraps
from flask import request, session
from flask.ext.restful import Resource, abort
from irianas_server.user import AuthSSH
from irianas_server.user import ManageUserServer
from irianas_server.models import \
    (RecordSession, Client, Event, RecordActionUser, HTTP, DNS, SSH, DATABASE,
     FTP)
from irianas_server.client import \
    ManageClient, ClientBasicTask, PutConfigService
from irianas_server.logs.logs_user import LogActionUser
from irianas_server.logs.logs_event_client import LogEventCLient

ip_server = socket.gethostbyname(socket.gethostname())


def requires_ssl(f):
    @wraps(f)
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
        return dict(status=1)

    @requires_ssl
    def post(self):
        return AuthSSH.login(request.form['user'], request.form['pass'])

    @check_token
    @requires_ssl
    def put(self, user):
        ses = RecordSession.objects(token=request.form.get('token'),
                                    user=user)
        if not ses:
            return abort(404)
        ses = ses[0]
        time = datetime.datetime.now() - datetime.timedelta(0, 3600)
        ses.token_end = time
        ses.save()
        return dict(action="Logout")


class InfoAPI(Resource):
    method_decorators = [requires_ssl, check_token]

    def get(self):
        data = dict(host_name=platform.node(),
                    arch=platform.machine(),
                    os=platform.version(),
                    memory=psutil.virtual_memory()[0])
        return data


# Manage User REST API
# ****** BEGIN ******


class UserAPI(Resource):
    """ API for the User System compare with User on Linux """
    ma = ManageUserServer()
    method_decorators = [requires_ssl, check_token]

    def get(self, action='list'):
        if action == 'list':
            users = self.ma.list_users()
            if users:
                return users
            else:
                return dict(status=0)
        elif action == 'expand':
            return self.ma.expand_time(request.form['username'],
                                       request.form['token'])
        else:
            return self.ma.time(request.form['username'],
                                request.form['token'])

    def post(self):
        if self.ma.add_user(request.form['user_system'],
                            request.form['password']):
            return dict(user=request.form['user_system'],
                        action=1)
        else:
            return dict(user=request.form['user_system'],
                        action=0)

    def put(self, action='update'):
        if action == 'update':
            if self.ma.update_user(request.form['user_system'],
                                   request.form['password']):
                return dict(user=request.form['user_system'],
                            action=1)
            else:
                return dict(user=request.form['user_system'],
                            action=0)
        else:
            if self.ma.delete_user(request.form['user_system']):
                return dict(user=request.form['user_system'],
                            action=1)
            else:
                return dict(user=request.form['user_system'],
                            action=0)

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
                    result.append(dict(ip=client.ip_address))
                return dict(result=result)
            else:
                return abort(404)
        else:
            client = Client.objects(ip_address=request.form['ip_address'])
            if client:
                client = client[0]
                return dict(ip_address=request.form['ip_address'])
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
    url = 'https://{ip}:9000/api/services/{services}/{action}'

    def get(self, services, action):
        try:
            client = Client.objects.get(ip_address=request.form['ip'])
        except mongoengine.DoesNotExist:
            return abort(404)

        token = client.token
        data = dict(ip=ip_server, token=token)
        url = self.url.format(services=services, action=action,
                              ip=request.form['ip'])

        r = requests.get(url, data=data, verify=False)
        if r.status_code == 200:
            # Logs and events
            LogActionUser.services_basic_actions(session['username'],
                                                 services, action)

            LogEventCLient.create_event(client, services, action, r.json())
            # ------------
            return r.json()
        else:
            return dict(error=0)


class ClientConfigServicesAPI(Resource):
    method_decorators = [requires_ssl, check_token]
    dict_services = dict(apache=HTTP, ssh=SSH, bind=DNS, vsftpd=FTP)

    def get(self):

        try:
            Client.objects.get(ip_address=request.form['ip'])
        except mongoengine.DoesNotExist:
            return abort(404)

        model = self.dict_services[request.form['service']]
        result = model.objects.get(client=request.form['ip']).to_json()
        return result

    def post(self):
        ip = request.form['ip']
        service = request.form['service']
        data = dict(request.form.items())

        # Delete unneccesary elements
        del(data['ip'])
        del(data['token'])
        del(data['service'])

        try:
            client = Client.objects.get(ip_address=ip)
        except mongoengine.DoesNotExist:
            return abort(404)

        token = client.token

        # Search the data
        model = self.dict_services[service]
        result = model.objects.get(client=ip)
        result.delete()

        model(last_change=datetime.datetime.now(),
              client=ip,
              **data).save()

        return PutConfigService.put_config_service(
            service, ip, data, token)


class EventAPI(Resource):
    method_decorators = [requires_ssl, check_token]

    def get(self):
        try:
            client = Client.objects.get(ip_address=request.form['ip'])
        except mongoengine.DoesNotExist:
            return abort(404)

        if client:
            events = Event.objects(client=client.id)[:4]
            events_comment = dict()
            for event in reversed(events):
                events_comment[event.date.strftime('%d/%m/%Y %H:%M:%S')] = \
                    event.comment

            return events_comment
        return abort(404)


class UserRecordAPI(Resource):
    method_decorators = [requires_ssl, check_token]

    def get(self):
        records = RecordActionUser.objects(user=session['username'])

        if records:
            return records.to_json()
        return abort(404)
