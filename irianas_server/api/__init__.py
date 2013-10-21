# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
from flask import (request)
from flask.ext.restful import Resource
from flask_login import login_required, login_user
from irianas_server.user import AuthSSH
from irianas_server.user import ManageUser, User as UserLogin


class Login(Resource):

    @login_required
    def get(self):
        return dict(login=1)

    def post(self):
        pass


class User(Resource):
    ma = ManageUser()

    @login_required
    def get(self):
        return dict(bien=1)
