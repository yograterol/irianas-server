# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import datetime
from mongoengine import \
    (Document, DateTimeField, StringField, ListField, ReferenceField,
     DecimalField, DynamicDocument)


# Database for irianas-web
class RecordSession(Document):
    user = StringField(max_length=50, required=True)
    date = DateTimeField(default=datetime.datetime.now())
    token = StringField()
    token_end = DateTimeField(default=datetime.datetime.now() +
                              datetime.timedelta(0, 900))
    meta = {'db_alias': 'irianas_web', 'collection': 'record_session'}


class RecordActionUser(Document):
    user = StringField(max_length=50, required=True)
    action = StringField(max_length=50, required=True)
    comment = StringField(max_length=100)
    date = DateTimeField(default=datetime.datetime.now())
    meta = {'db_alias': 'irianas_web', 'collection': 'record_action_user'}


# Database for irianas-server
class Client(Document):
    ip_address = StringField(max_length=50, required=True)
    services_install = ListField()
    token = StringField()
    token_end = DateTimeField(default=datetime.datetime.now() +
                              datetime.timedelta(0, 100800))
    meta = {'db_alias': 'irianas_web'}


class LogResource(Document):
    client = ReferenceField('Client')
    date = DateTimeField(default=datetime.datetime.now())
    cpu = DecimalField()
    memory = DecimalField()
    disk = DecimalField()
    meta = {'db_alias': 'irianas_web', 'collection': 'client.log_resource'}


class SettingService(Document):
    client = ReferenceField('Client')
    meta = {'db_alias': 'irianas_web', 'collection': 'client.setting_service'}


class HTTP(DynamicDocument):
    last_change = DateTimeField(default=datetime.datetime.now(), required=True)
    client = ReferenceField('SettingService')
    meta = {'db_alias': 'irianas_web',
            'collection': 'client.setting_service.http'}


class FTP(DynamicDocument):
    last_change = DateTimeField(default=datetime.datetime.now(), required=True)
    client = ReferenceField('SettingService')
    meta = {'db_alias': 'irianas_web',
            'collection': 'client.setting_service.ftp'}


class DNS(DynamicDocument):
    last_change = DateTimeField(default=datetime.datetime.now(), required=True)
    client = ReferenceField('SettingService')
    meta = {'db_alias': 'irianas_web',
            'collection': 'client.setting_service.dns'}


class EMAIL(DynamicDocument):
    last_change = DateTimeField(default=datetime.datetime.now(), required=True)
    client = ReferenceField('SettingService')
    meta = {'db_alias': 'irianas_web',
            'collection': 'client.setting_service.email'}


class DATABASE(DynamicDocument):
    last_change = DateTimeField(default=datetime.datetime.now(), required=True)
    client = ReferenceField('SettingService')
    meta = {'db_alias': 'irianas_web',
            'collection': 'client.setting_service.database'}
