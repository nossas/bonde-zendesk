#!/usr/bin/env python
# coding: utf-8
from logger import log
from decorators import decode_jwt
from serializers import FormEntry, User
from settings import api

MAPPING_FIELDS_UID = {
    # Required fields to user Zendesk
    'name': 'field-1531256279518-15',
    'email': 'field-1531256284908-34',
    # Custom fields on Zendesk
    'state': 'field-1531256429599-79',
    'city': 'field-1531256438968-91',
    'neighborhood': 'field-1531256466688-98',
    'tipo_de_acolhimento': 'field-1531256486749-86'
}

MAPPING_ORGANIZATIONS_ID = {
    'MSR': 360273031591,
    'Psicologa': 360261425772,
    'Advogada': 360269610652
}


@decode_jwt(serializer_class=FormEntry)
def send_form_entry_to_zendesk(form_entry):
    """Create User on Zendesk API"""
    # from settings import api

    def filter_fields(uid):
        return list(filter(lambda x: x.uid == uid, form_entry.xfields))[0]

    # resp = api.users().post(data=dict(user=user.as_json()))
    # TODO: what to do from here?
    attrs = {
        'role': 'end-user',
        # Add default attrs to create a MSR user on Zendesk
        'organization_id': MAPPING_ORGANIZATIONS_ID.get('MSR'),
        'user_fields': {}
    }

    # loop in fixed user fields
    for field_name in ['name', 'email']:
        field = filter_fields(MAPPING_FIELDS_UID.get(field_name))
        attrs[field_name] = field.value

    # insert custom user fields for MSR
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
            'psicológico_e_jurídico')

    # validate instance of user filled ok.
    user = User(**attrs)
    body = dict(user=user.__dict__)

    log.info('Request [POST] Zendesk API')
    try:
        resp = api.users().post(data=body)
        return resp
    except Exception as err:
        log.error('Request [POST] Zendesk API failed.')
        log.error(err)


if __name__ == '__main__':
    send_form_entry_to_zendesk()


# Custom user fields on Zendesk:
# condition, address, city, tipo_de_acolhimento, latitude, longitude
# whatsapp, registration_number, occupation_area,
# disponibilidade_de_atendimentos encaminhamentos,
# atendimentos_em_andamento, state
#
# Tipos de acolhimento v1: ['atendimento_']
# Tipos de acolhimento v2: ['psicológico', 'jurídico', 'psicológico_e_jurídico']
