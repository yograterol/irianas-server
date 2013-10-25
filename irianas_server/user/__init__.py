# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import os
import datetime
from paramiko import (SSHClient, WarningPolicy, AuthenticationException)
from irawadi_user import ManageUser
from irawadi_user import UserExist, UserNotExist
from irianas_server.models import RecordSession


class AuthSSH(object):
    """ Class for sign in the user with system user"""

    @staticmethod
    def login(username, password):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(WarningPolicy())
        try:
            client.connect('localhost', username=username, password=password,
                           port=22)

            rs = RecordSession(user=username)
            rs.token = os.urandom(64).encode('hex')
            rs.date = datetime.datetime.now()
            rs.token_end = datetime.datetime.now() + datetime.timedelta(0, 900)
            rs.save()

            return dict(token=rs.token, user=username)
        except AuthenticationException:
            return dict(login=0)

# Start the ManageUserServer class
ma = ManageUser()


class ManageUserServer(object):
    """ Create user in the system, without permissions and without shell """

    @staticmethod
    def add_user(username, password):
        try:
            if ma.create(user=username, p=password, M='', N='',
                         s='/sbin/nologin'):
                return True
            else:
                return False
        except UserExist:
            return False

    @staticmethod
    def update_user(username, password):
        try:
            if ma.update_password(user=username, password=password):
                return True
            else:
                return False
        except UserNotExist:
            return False

    @staticmethod
    def delete_user(username):
        try:
            if ma.delete(username):
                return True
            else:
                return False
        except UserNotExist:
            return False
