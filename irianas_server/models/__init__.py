# This file is part of Irianas (Server).
# Copyright (C) 2013 Irisel Gonzalez.
# Authors: Irisel Gonzalez <irisel.gonzalez@gmail.com>
#
import datetime
from mongoengine import \
    (Document, DateTimeField, StringField, ReferenceField,
     DecimalField, DynamicDocument, IntField)


# Database for irianas-web
class RecordSession(Document):
    user = StringField(max_length=50, required=True)
    date = DateTimeField(default=datetime.datetime.now())
    token = StringField()
    token_end = DateTimeField()
    meta = {'db_alias': 'irianas_web', 'collection': 'record_session'}


class RecordActionUser(Document):
    user = StringField(max_length=50, required=True)
    action = StringField(max_length=50, required=True)
    comment = StringField(max_length=100)
    date = DateTimeField()
    meta = {'db_alias': 'irianas_web', 'collection': 'record_action_user'}


# Database for irianas-server
class Client(Document):
    ip_address = StringField(max_length=50, required=True, unique=True)
    token = StringField()
    meta = {'db_alias': 'irianas_server', 'collection': 'client',
            'indexes': ['ip_address']}


class LogResource(Document):
    client = ReferenceField('Client')
    date = DateTimeField()
    cpu = DecimalField()
    memory = DecimalField()
    disk = DecimalField()
    meta = {'db_alias': 'irianas_server', 'collection': 'client.log_resource'}


class Event(Document):
    client = ReferenceField('Client')
    date = DateTimeField()
    type_event = IntField(min_value=1, max_value=3)
    comment = StringField(max_length=100)
    meta = {'db_alias': 'irianas_server', 'collection': 'client.event',
            'ordering': ['-date']}


class HTTP(DynamicDocument):
    last_change = DateTimeField()
    client = StringField(max_length=100)
    meta = {'db_alias': 'irianas_server',
            'collection': 'client.setting_service.http'}


class FTP(DynamicDocument):
    last_change = DateTimeField()
    client = StringField(max_length=100)
    meta = {'db_alias': 'irianas_server',
            'collection': 'client.setting_service.ftp'}


class DNS(DynamicDocument):
    last_change = DateTimeField()
    client = StringField(max_length=100)
    meta = {'db_alias': 'irianas_server',
            'collection': 'client.setting_service.dns'}


class SSH(DynamicDocument):
    last_change = DateTimeField()
    client = StringField(max_length=100)
    meta = {'db_alias': 'irianas_server',
            'collection': 'client.setting_service.ssh'}


class DATABASE(DynamicDocument):
    last_change = DateTimeField()
    client = StringField(max_length=100)
    meta = {'db_alias': 'irianas_server',
            'collection': 'client.setting_service.database'}
