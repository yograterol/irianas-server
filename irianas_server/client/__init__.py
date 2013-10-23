import requests
from flask import request
from flask_restful import abort
from irianas_server.models import Client, LogResource

url_client = 'https://{ip}:9000/connection'
url_client = 'https://{ip}:9000/api/task/{action}'


class ManageClient(object):

    @staticmethod
    def connect_client():
        url = url_client.format(ip=request.form['ip'])
        req = requests.get(url)
        if req.status_code == 200:
            result = req.json()
            client = Client(ip_address=request.form['ip'])
            client.token = result['token']
            client.save()

            return dict(client=request.form['ip'], status="Connected")
        else:
            return dict(client=request.form['ip'], status="NotConnected")

    @staticmethod
    def delete_client():
        url = url_client.format(ip=request.form['ip'])
        req = requests.get(url)
        if req.status_code == 200:
            result = req.json()
            if result.get('status') == 'Deleted':
                client = Client.objects(ip_address=request.form['ip'])[0]
                client.remove()
                return dict(client='Deleted')
        return dict(client='NotDeleted')


class ClientBasicTask(object):

    @staticmethod
    def request_task(action):
        if action == 'monitor':
            url = url_client.format(ip=request.form['ip'], action=action)
            req = requests.get(url)
            if req.status_code == 200:
                result = req.json()

                lg = LogResource()
                client = Client.objects(ip_address=request.form['ip'])[0]
                lg.client = client
                lg.cpu = result['cpu']
                lg.memory = result['memory']
                lg.disk = result['disk']
                lg.save()

                return result
        elif action in ['shut', 'reboot', 'hibernate']:
            url = url_client.format(ip=request.form['ip'], action=action)
            req = request.get(url)
            return dict(status='Sended')
        return abort(500)
