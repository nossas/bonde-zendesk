#!/usr/bin/env python
# coding: utf-8
from logger import log
from decorators import decode_jwt
from geolocation import get_geocode
from serializers import FormEntrySchema, UserSchema
from settings import zendesk

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


@decode_jwt(serializer_class=FormEntrySchema)
def send_form_entry_to_zendesk(form_entry):
    """Create User on Zendesk API"""

    def filter_fields(uid):
        return list(filter(lambda x: x.uid == uid, form_entry.fields))[0]

    # Fill fields on User Zendesk.
    organization = None
    if form_entry.widget_id == 16850:
        organization = 'MSR'
    elif form_entry.widget_id == 17628:
        organization = 'Psicologa'
    elif form_entry.widget_id == 17633:
        organization = 'Advogada'

    attrs = {
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

    # search geocode
    adrr = '{address}, {city} - {state}'.format(**attrs['user_fields'])
    geocode = get_geocode(adrr)

    attrs['user_fields']['address'] = geocode.formatted_address
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

    return user


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
