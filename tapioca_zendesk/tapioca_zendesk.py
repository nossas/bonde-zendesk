# coding: utf-8

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class ZendeskClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://mapadoacolhimento.zendesk.com/api/v2/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(ZendeskClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        auth = (api_params.get('user') + '/token', api_params.get('password'))
        params['auth'] = auth

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass


Zendesk = generate_wrapper_from_adapter(ZendeskClientAdapter)
