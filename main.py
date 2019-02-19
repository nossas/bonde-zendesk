#!/usr/bin/env python
# coding: utf-8
from logger import log
from decorators import decode_jwt
from runners import Organization, MSRRunner
from serializers import FormEntrySchema


@decode_jwt(serializer_class=FormEntrySchema)
def send_form_entry_to_zendesk(form_entry):
    """Create User on Zendesk API"""

    if Organization.be(form_entry) == Organization.MSR:
        runner = MSRRunner(form_entry)
        user, tickets = runner.execute()
        return user, tickets

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
