from .psicologa import Runner as PsicologaRunner


class Runner(PsicologaRunner):
    __MAPPING_FIELDS_UID__ = {
        # Concat {first_name}{last_name} to user.name
        'first_name': 'field-1533735738039-59',
        'last_name': 'field-1533735745400-14',
        'email': 'field-1533735752669-39',
        'phone': 'field-1533735813563-2',
        # Custom fields on Zendesk
        # 'state': 'field-1533735770558-86',
        # 'city': 'field-1533735788159-99',
        'address': 'field-1533735803691-45',
        'registration_number': 'field-1533735761357-93',
        'whatsapp': 'field-1533735832329-53',
        # 'occupation_area': 'field-1533735911227-68',
        'disponibilidade_de_atendimentos': 'field-1533735888966-20',
    }
