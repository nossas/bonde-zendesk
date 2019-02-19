from .base import RunnerInterface, Organization


class Runner(RunnerInterface):
    __MAPPING_FIELDS_UID__ = {
        # Concat {first_name}{last_name} to user.name
        'first_name': 'field-1533733461113-5',
        'last_name': 'field-1533733485653-99',
        'email': 'field-1533733493037-11',
        'phone': 'field-1533734419113-13',
        # Custom fields on Zendesk
        'state': 'field-1533733516193-68',
        'city': 'field-1533733622959-48',
        'address': 'field-1533733650118-7',
        'registration_number': 'field-1533733501716-34',
        'whatsapp': 'field-1533734468460-38',
        'occupation_area': 'field-1533734520150-2',
        'disponibilidade_de_atendimentos': 'field-1533734495315-40',
    }

    def prepare_user_attrs(self):
        if Organization.be(self.form_entry) != Organization.MSR:
            attrs = {
                'external_id': self.form_entry.id,
                'role': 'end-user',
                # Add default attrs to create a MSR user on Zendesk
                'organization_id': Organization.id(self.form_entry),
                'user_fields': {'condition': 'desabilitada'}
            }

            # loop in fixed user fields
            attrs['name'] = '{first_name} {last_name}'.format(
                first_name=self._filter_fields('first_name').value,
                last_name=self._filter_fields('last_name').value)

            for field_name in ['email', 'phone']:
                field = self._filter_fields(field_name)
                attrs[field_name] = field.value

            # insert custom user fields for MSR
            field = self._filter_fields('state')
            attrs['user_fields']['state'] = field.value.lower()

            for field_name in [
                'city', 'address', 'registration_number', 'whatsapp',
                'occupation_area', 'disponibilidade_de_atendimentos'
            ]:
                field = self._filter_fields(field_name)
                attrs['user_fields'][field_name] = field.value

            # search geocode
            geocode = self._address(attrs)

            # update with geocode info
            attrs['user_fields']['address'] = geocode.formatted_address
            attrs['user_fields']['state'] = geocode.state.lower()
            attrs['user_fields']['latitude'] = geocode.geometry.location.lat
            attrs['user_fields']['longitude'] = geocode.geometry.location.lng

            return attrs

    def prepare_tickets_attrs(self, user):
        # Not necessary impletment this method, PSICOLOGA subscribe aways
        # like desabilitada
        pass
