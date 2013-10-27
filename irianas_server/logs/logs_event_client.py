import datetime
from irianas_server.models import Event


class LogEventCLient(object):

    @staticmethod
    def create_event(client, service, action, result):
        actions = dict(
            start="Se Activ&oacute el servicio {service}",
            stop="Se Detuvo el servicio {service}",
            install="Se instal&oacute; {service})",
            remove="Se desinstal&oacute; {service}")

        if action in actions.keys():
            if action is 'install' or action is 'remove':
                type_event = 1
            else:
                type_event = 2

            event = Event()
            event.client = client
            event.date = datetime.datetime.now()
            event.type_event = type_event
            event.comment = actions[action].format(service=service)
            event.save()
