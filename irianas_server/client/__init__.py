import requests
from flask import request
from irianas_server.models import Client


class ManageClient(object):

    @staticmethod
    def connect_client():
        url = 'https://{ip}:9000/connection'.format(ip=request.form['ip'])
        req = requests.get(url)
        if req.status_code == 200:
            result = req.json()
            client = Client(ip_address=request.form['ip'])
            client.token = result['token']
            client.save()

            return dict(client=request.form['ip'], status="Connected")
        else:
            return dict(client=request.form['ip'], status="NotConnected")
