# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
from flask_login import UserMixin
from paramiko import (SSHClient, WarningPolicy, AuthenticationException)
from irawadi_user import ManageUser as ma
from irawadi_user import UserExist, UserNotExist


class User(UserMixin):

    def __init__(self, name, id):
        self.name = name
        self.id = id


class AuthSSH(object):

    @staticmethod
    def login(username, password):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(WarningPolicy())
        try:
            client.connect('localhost', username=username, password=password)
            return True
        except AuthenticationException:
            return False


class ManageUser(object):

    @staticmethod
    def add_user(username, password):
        try:
            if ma.create(username, password):
                return True
            else:
                return False
        except UserExist:
            return False

    @staticmethod
    def update_user(username, password):
        try:
            if ma.update_password(username, password):
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
