import datetime
from irianas_server.models import RecordActionUser


class LogActionUser(object):

    @staticmethod
    def services_basic_actions(user, service, action):
        actions = dict(
            installed="Verific&oacute; la instalaci&oacute;n de: {service})",
            start="Activ&oacute el servicio {service}",
            stop="Detuvo el servicio {service}",
            install="Solicit&oacute; la instalaci&oacute;n de {service}",
            remove="Solicit&oacute; la desinstalaci&oacute;n de {service}",
            status="Verific&oacute; el estado de {service}")
        action_text = actions[action]

        record = RecordActionUser(user=user, action=action)
        record.date = datetime.datetime.now()
        record.comment = action_text.format(service=service)
        record.save()
