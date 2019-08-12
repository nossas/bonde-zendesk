#!/usr/bin/env python
# coding: utf-8
from flask import Flask
from flask import request
from serializers import FormEntrySchema
import json
from runners import (
    Organization, MSRRunner, PsicologaRunner, AdvogadaRunner
)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()['event']['data']['new']

        if data['fields']:
            data['fields'] = json.loads(data['fields'])

        instance = FormEntrySchema().load(data)
        form_entry = instance.data

        runner = None
        user = None
        if Organization.be(form_entry) == Organization.MSR:
            runner = MSRRunner(form_entry, "")
        elif Organization.be(form_entry) == Organization.PSICOLOGA:
            runner = PsicologaRunner(form_entry, "")
        elif Organization.be(form_entry) == Organization.ADVOGADA:
            runner = AdvogadaRunner(form_entry, "")

        if runner:
            user = runner.execute()
            return 'OK'

        return "Organization isn't MSR, Psicologa, \
            Advogada, bonde-zendesk not parse others organizations."
