#!/usr/bin/env python
# coding: utf-8
from logger import log
from decorators import decode_jwt
from runners import (
    Organization, MSRRunner, PsicologaRunner, AdvogadaRunner
)
from serializers import FormEntrySchema


@decode_jwt(serializer_class=FormEntrySchema)
def send_form_entry_to_zendesk(form_entry, token):
    """Create User on Zendesk API"""
    runner = None
    if Organization.be(form_entry) == Organization.MSR:
        runner = MSRRunner(form_entry, token)
    elif Organization.be(form_entry) == Organization.PSICOLOGA:
        runner = PsicologaRunner(form_entry, token)
    elif Organization.be(form_entry) == Organization.ADVOGADA:
        runner = AdvogadaRunner(form_entry, token)

    if runner:
        return runner.execute()

    log.error("[Bonde/Zendesk] Organization isn't MSR, Psicologa, \
        Advogada, bonde-zendesk not parse others organizations.")


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
