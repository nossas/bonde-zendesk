#!/usr/bin/env python
# coding: utf-8
from logger import log
from decorators import decode_jwt
from geolocation import get_geocode
from serializers import FormEntrySchema, UserSchema, TicketSchema
from settings import zendesk

MAPPING_FIELDS_UID = {
    # Required fields to user Zendesk
    'name': 'field-1531256279518-15',
    'email': 'field-1531256284908-34',
    # Custom fields on Zendesk
    'state': 'field-1531256429599-79',
    'city': 'field-1531256438968-91',
    'neighborhood': 'field-1531256466688-98',
    'tipo_de_acolhimento': 'field-1531256486749-86',
    'has_condition': 'field-1546881946816-20'
}

MAPPING_ORGANIZATIONS_ID = {
    'MSR': 360273031591,
    'Psicologa': 360282119532,
    'Advogada': 360269610652
}

MSR = 'MSR'
PSICOLOGA = 'Psicologa'
ADVOGADA = 'Advogada'


@decode_jwt(serializer_class=FormEntrySchema)
def send_form_entry_to_zendesk(form_entry):
    """Create User on Zendesk API"""

    def filter_fields(uid):
        return list(filter(lambda x: x.uid == uid, form_entry.fields))[0]

    # Fill fields on User Zendesk.
    organization = None
    if form_entry.widget_id == 16850:
        organization = MSR
    elif form_entry.widget_id == 17628:
        organization = PSICOLOGA
    elif form_entry.widget_id == 17633:
        organization = ADVOGADA

    if organization == MSR:
        attrs = {
            'external_id': form_entry.id,
            'role': 'end-user',
            # Add default attrs to create a MSR user on Zendesk
            'organization_id': MAPPING_ORGANIZATIONS_ID.get(organization),
            'user_fields': {}
        }

        # loop in fixed user fields
        for field_name in ['name', 'email']:
            field = filter_fields(MAPPING_FIELDS_UID.get(field_name))
            attrs[field_name] = field.value

        # insert custom user fields for MSR
        try:
            field = filter_fields(MAPPING_FIELDS_UID.get('has_condition'))
            attrs['user_fields']['condition'] = 'inscrita' \
                if field.value.lower() == 'sim' else 'desabilitada'
        except IndexError:
            # IndexError happens when update an older form_entries (MSR).
            attrs['user_fields']['condition'] = 'inscrita'

        field = filter_fields(MAPPING_FIELDS_UID.get('state'))
        attrs['user_fields']['state'] = field.value.lower()

        field = filter_fields(MAPPING_FIELDS_UID.get('city'))
        attrs['user_fields']['city'] = field.value

        field = filter_fields(MAPPING_FIELDS_UID.get('neighborhood'))
        attrs['user_fields']['address'] = field.value

        field = filter_fields(MAPPING_FIELDS_UID.get('tipo_de_acolhimento'))
        attrs['user_fields']['tipo_de_acolhimento'] = field.value\
            .replace('Acolhimento Jurídico', 'jurídico')\
            .replace('Acolhimento Terapêutico', 'psicológico')\
            .replace(
                'Acolhimento Terapêutico & Jurídico',
                'psicológico_e_jurídico')\
            .replace('psicológico & Jurídico', 'psicológico_e_jurídico')

        # search geocode
        adrr = '{address}, {city} - {state}'.format(**attrs['user_fields'])
        geocode = get_geocode(adrr)

        # update with geocode info
        attrs['user_fields']['address'] = geocode.formatted_address
        attrs['user_fields']['state'] = geocode.state.lower()
        attrs['user_fields']['latitude'] = geocode.geometry.location.lat
        attrs['user_fields']['longitude'] = geocode.geometry.location.lng

        # validate instance of user filled ok.
        serializer = UserSchema()
        payload = dict(user=serializer.dump(attrs).data)

        response = zendesk.user_create_or_update().post(data=payload)
        # update user with data response
        user = serializer.load(response().data['user']).data

        log.info('[Zendesk] Create / Update user #{0} on {1}.'.format(
            user.id, organization))

        # Create a ticket on Zendesk
        prefix_tickets = [user.user_fields.tipo_de_acolhimento]
        if user.user_fields.tipo_de_acolhimento == 'psicológico_e_jurídico':
            prefix_tickets = ['psicológico', 'jurídico']

        tickets = []
        for prefix in prefix_tickets:
            attrs = {
                'subject': '[{0}] {1}'.format(
                    prefix, form_entry.widget_settings.email_subject),
                'requester_id': user.id,
                'custom_fields': []
            }
            attrs['description'] = 'teste'
            attrs['comment'] = dict(body=form_entry.widget_settings.email_text)
            attrs['custom_fields'].append(
                dict(id=360016681971, value=user.name)
            )
            tickets.append(attrs)

        serializer = TicketSchema(many=True)
        payload = dict(tickets=serializer.dump(tickets).data)
        response = zendesk.create_many_tickets().post(data=payload)
        # update ticket with data response
        log.info('[Zendesk] Create job to create tickets. {0}'.format(
            response().data['job_status']['url']))

        return user

    log.error("[Bonde/Zendesk] Organization isn't MSR, bonde-zendesk \
        not parse others organizations.")


if __name__ == '__main__':
    send_form_entry_to_zendesk()


# Custom user fields on Zendesk:
# condition, address, city, tipo_de_acolhimento, latitude, longitude
# whatsapp, registration_number, occupation_area,
# disponibilidade_de_atendimentos encaminhamentos,
# atendimentos_em_andamento, state
#
# Tipo de acolhimento v1: ['atendimento_']
# Tipo de acolhimento v2: ['psicológico', 'jurídico', 'psicológico_e_jurídico']
