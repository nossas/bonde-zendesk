from .base import RunnerInterface, Organization


class Runner(RunnerInterface):
    __MAPPING_FIELDS_UID__ = {
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

    def prepare_user_attrs(self):
        if Organization.be(self.form_entry) == Organization.MSR:
            attrs = {
                'role': 'end-user',
                # Add default attrs to create a MSR user on Zendesk
                'organization_id': Organization.id(self.form_entry),
                'user_fields': {}
            }

            # loop in fixed user fields
            for field_name in ['name', 'email']:
                field = self._filter_fields(field_name)
                attrs[field_name] = field.value

            # insert custom user fields for MSR
            try:
                field = self._filter_fields('has_condition')
                attrs['user_fields']['condition'] = 'inscrita' \
                    if field.value.lower() == 'sim' else 'desabilitada'
            except IndexError:
                # IndexError happens when update an older form_entries (MSR).
                attrs['user_fields']['condition'] = 'inscrita'

            field = self._filter_fields('state')
            attrs['user_fields']['state'] = field.value.lower()

            field = self._filter_fields('city')
            attrs['user_fields']['city'] = field.value

            field = self._filter_fields('neighborhood')
            attrs['user_fields']['address'] = field.value

            field = self._filter_fields('tipo_de_acolhimento')
            attrs['user_fields']['tipo_de_acolhimento'] = field.value\
                .replace('Acolhimento Jurídico', 'jurídico')\
                .replace('Acolhimento Terapêutico', 'psicológico')\
                .replace(
                    'Acolhimento Terapêutico & Jurídico',
                    'psicológico_e_jurídico')\
                .replace('psicológico & Jurídico', 'psicológico_e_jurídico')\
                .replace('Psicológico & Jurídico', 'psicológico_e_jurídico')

            # search geocode
            geocode = self._address(attrs)

            # update with geocode info
            attrs['user_fields']['address'] = geocode.formatted_address
            attrs['user_fields']['state'] = geocode.state.lower()
            attrs['user_fields']['latitude'] = geocode.geometry.location.lat
            attrs['user_fields']['longitude'] = geocode.geometry.location.lng

            return attrs

    def prepare_tickets_attrs(self, user):
        prefix_tickets = [user.user_fields.tipo_de_acolhimento]
        if user.user_fields.tipo_de_acolhimento == 'psicológico_e_jurídico':
            prefix_tickets = ['psicológico', 'jurídico']

        tickets = []
        for prefix in prefix_tickets:
            fargs = dict(
                prefix=prefix.capitalize(), name=user.name,
                city=user.user_fields.city, uf=user.user_fields.state.upper())

            attrs = {
                'subject': '[{prefix}] {name}, {city} - {uf}'.format(**fargs),
                'requester_id': user.id,
                'custom_fields': []
            }
            attrs['external_id'] = self.form_entry.id
            attrs['comment'] = dict(body='Importado pelo BONDE.')
            attrs['custom_fields'].append(
                dict(id=360016681971, value=user.name))
            attrs['custom_fields'].append(
                dict(id=360014379412, value='solicitação_recebida'))
            tickets.append(attrs)

        return tickets
