import requests
import mongoengine
import socket
import datetime
from flask import request
from flask_restful import abort
from irianas_server.models import Client, LogResource

ip_server = socket.gethostbyname(socket.gethostname())

url_client = 'https://{ip}:9000/api/connect'
url_client_task = 'https://{ip}:9000/api/task/{action}'


class ManageClient(object):

    @staticmethod
    def connect_client():
        url = url_client.format(ip=request.form['ip'])
        try:
            req = requests.post(
                url, data=dict(ip=ip_server),
                verify=False)
        except requests.ConnectionError:
            return abort(404)

        if req.status_code == 200:
            result = req.json()
            try:
                client = Client.objects.get(ip_address=request.form['ip'])
            except mongoengine.DoesNotExist:
                client = Client(ip_address=request.form['ip'])

            client.token = result['token']

            if client.save():
                return dict(status=1)
            else:
                return dict(status=-1)
        elif req.status_code == 401:
            return dict(status=-1)
        return dict(status=0)

    @staticmethod
    def delete_client():
        client = None
        try:
            client = Client.objects.get(ip_address=request.form['ip'])
        except mongoengine.DoesNotExist:
            return abort(404)

        token = client.token

        try:
            url = url_client.format(ip=request.form['ip'])
            req = requests.get(url, data=dict(ip=ip_server, token=token),
                               verify=False)
        except requests.ConnectionError:
            return abort(404)

        if req.status_code == 200:
            result = req.json()
            if result.get('logout') == 1:
                client.delete()
                return result
        return (406)


class ClientBasicTask(object):

    @staticmethod
    def request_task(action):
        ip = request.form['ip']
        try:
            client = Client.objects.get(ip_address=ip)
        except mongoengine.DoesNotExist:
            return abort(404)

        token = client.token
        data = dict(ip=ip_server, token=token)

        if action == 'monitor':
            try:
                url = url_client_task.format(ip=ip, action=action)
                req = requests.get(url, data=data, verify=False)
            except requests.ConnectionError:
                return abort(404)

            if req.status_code == 200:
                result = req.json()

                lg = LogResource()
                lg.client = client
                lg.cpu = result['cpu']
                lg.memory = result['memory']
                lg.disk = result['disk']
                lg.date = datetime.datetime.now()
                lg.save()

                return result
        elif action in ['shut', 'reboot', 'hibernate']:
            try:
                url = url_client_task.format(ip=ip, action=action)
                req = requests.get(url, data=data, verify=False)
            except requests.ConnectionError:
                return abort(404)
            return dict(status=1)
        elif action == 'info':
            try:
                url = url_client_task.format(ip=ip, action=action)
                req = requests.get(url, data=data, verify=False)
            except requests.ConnectionError:
                return abort(404)

            if req.status_code == 200:
                return req.json()
            return abort(404)
        return abort(500)
