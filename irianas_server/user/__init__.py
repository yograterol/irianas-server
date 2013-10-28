# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import os
import datetime
import subprocess as sub
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
    def check_user_valid(username):
        users = ManageUserServer.list_users()
        if users:
            if not username in users['users']:
                return True
        return False

    @staticmethod
    def expand_time(username, token):
        rs = RecordSession.objects.get(user=username, token=token)
        if rs:
            rs.token_end += datetime.timedelta(0, 900)
            token_end = rs.token_end - datetime.datetime.now()
            if token_end <= datetime.timedelta(0, 1800):
                rs.save()
                return dict(status=1)
        return dict(status=0)

    @staticmethod
    def time(username, token):
        rs = RecordSession.objects.get(user=username, token=token)

        if rs:
            time_token = rs.token_end - datetime.datetime.now()
            return dict(time=str(time_token))
        return dict(status=0)

    @staticmethod
    def list_users():
        cmd = 'awk -F\':\' -v "min=1000" -v "max=2000" \'\
              { if ( $3 >= min && $3 <= max ) print $1}\' /etc/passwd'
        action = sub.Popen(cmd, stdout=sub.PIPE, shell=True)
        (output, error) = action.communicate()

        if output:
            users_dict = dict()
            users_dict["users"] = list()
            for user in output.split('\n'):
                if user:
                    users_dict["users"].append(user)
            return users_dict
        return None

    @staticmethod
    def add_user(username, password):
        try:
            if ManageUserServer.check_user_valid(username):
                if ma.create(user=username, p=password, M='', N='',
                             s='/sbin/nologin'):
                    return True
                else:
                    return False
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
