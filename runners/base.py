from serializers import UserSchema, TicketSchema
from geolocation import get_geocode
from logger import log
from settings import zendesk


class Organization:
    MSR = 'MSR'
    PSICOLOGA = 'Psicologa'
    ADVOGADA = 'Advogada'

    __MAPPING_ORGANIZATIONS_ID__ = {
        MSR: 360273031591,
        PSICOLOGA: 360282119532,
        ADVOGADA: 360269610652
    }

    @classmethod
    def be(cls, form_entry):
        if form_entry.widget_id == 16850:
            return cls.MSR
        elif form_entry.widget_id == 17628:
            return cls.PSICOLOGA
        elif form_entry.widget_id == 17633:
            return cls.ADVOGADA

    @classmethod
    def id(cls, form_entry):
        if form_entry.widget_id == 16850:
            return cls.__MAPPING_ORGANIZATIONS_ID__.get(cls.MSR)
        elif form_entry.widget_id == 17628:
            return cls.__MAPPING_ORGANIZATIONS_ID__.get(cls.PSICOLOGA)
        elif form_entry.widget_id == 17633:
            return cls.__MAPPING_ORGANIZATIONS_ID__.get(cls.ADVOGADA)


class RunnerInterface(object):
    __MAPPING_FIELDS_UID__ = None

    def __init__(self, form_entry):
        self.form_entry = form_entry

    def _filter_fields(self, fieldName):
        assert self.__MAPPING_FIELDS_UID__ is not None, \
            '__MAPPING_FIELDS_UID__ should be configured.'
        uid = self.__MAPPING_FIELDS_UID__.get(fieldName)
        return list(filter(lambda x: x.uid == uid, self.form_entry.fields))[0]

    def _address(self, attrs):
        adrr = '{address}, {city} - {state}'.format(**attrs['user_fields'])
        return get_geocode(adrr)

    def prepare_user_attrs(self):
        raise NotImplementedError('Should be implement execute method.')

    def _send_user_zendesk(self, attrs):
        # validate instance of user filled ok.
        serializer = UserSchema()
        payload = dict(user=serializer.dump(attrs).data)

        response = zendesk.user_create_or_update().post(data=payload)
        # update user with data response
        user = serializer.load(response().data['user']).data

        log.info('[Zendesk] Create / Update user #{0} on {1}.'.format(
            user.id, Organization.be(self.form_entry)))

        return user

    def prepare_tickets_attrs(self, user):
        raise NotImplementedError('Should be implement execute method.')

    def _send_tickets_zendesk(self, tickets):
        # Create a ticket on Zendesk
        serializer = TicketSchema(many=True)
        payload = dict(tickets=serializer.dump(tickets).data)
        response = zendesk.create_many_tickets().post(data=payload)

        # update ticket with data response
        log.info('[Zendesk] Create job to create tickets. {0}'.format(
            response().data['job_status']['url']))

        return tickets

    def _check_tickts_exists(self):
        params = dict(external_id=self.form_entry.id)
        response = zendesk.tickets().get(params=params)

        return len(response().data['tickets']) > 0

    def execute(self):
        attrs = self.prepare_user_attrs()
        user = self._send_user_zendesk(attrs)
        if user.user_fields.condition != 'desabilitada' \
                and not self._check_tickts_exists():
            # Insert only new tickets
            attrs = self.prepare_tickets_attrs(user)
            tickets = self._send_tickets_zendesk(attrs)
            return user, tickets
        return user
