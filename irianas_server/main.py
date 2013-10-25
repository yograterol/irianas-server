#!/usr/bin/env python
""":mod:`irianas_server.main` -- Program entry point
"""
import sys
sys.path[0:0] = [""]
import os
from OpenSSL import SSL
from mongoengine import register_connection
from irianas_server.core import build_app
from irianas_server import app


debug = False
path = None

if 'VIRTUAL_ENV' in os.environ:
    path = os.path.join(os.environ['VIRTUAL_ENV'], 'ssl-demo')
    debug = True
else:
    path = '/etc/ssl/certs/'
    debug = False

try:
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file(os.path.join(path, 'server.key'))
    context.use_certificate_file(os.path.join(path, 'server.crt'))
except SSL.Error:
    context = None


def main():
    app.secret_key = 'as90kSDKO#1@|4245losadim'
    build_app(app)
    register_connection('irianas_web', 'irianas_web')

    app.run(debug=debug, ssl_context=context, host='0.0.0.0', port=9001)

if __name__ == '__main__':
    main()
