from zeep import Client, xsd
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
import zeep.cache
import zeep.transports
from .mappings import query_type_mapping, cvd_field_mapping, layer_field_mapping, collection_field_mapping, pending_device_field_mapping, policy_field_mapping, volume_field_mapping
from .queries import _collect_query_results


class VmwareMirageClient():
    def __init__(self, server, username, password, port=7443, cache=zeep.cache.InMemoryCache()):
        transport = zeep.transports.Transport(cache=cache)
        self.history = HistoryPlugin()
        self.client = Client("https://{}:{}/mirageapi/MitService.svc?singleWsdl".format(server, port), plugins=[self.history], transport=transport)

        self.username = username
        self.password = password
        try:
            login_response = self.client.service.Login(username=username, password=password)
        except Fault as e:
            raise e.message

        self.query_factory = self.client.type_factory('vmware.mirage.mit.query')
        self.type_factory = self.client.type_factory('vmware.mirage.mit.types')


    def get_cvds(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = cvd_field_mapping[by]
        cvds = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Cvd_Query
            )
        return cvds


    def get_cvd(self, id):
        result = self.client.service.Cvd_Get(id=id)
        return result


    def get_collection_cvds(self, collection_id, by='NAME', value='', query_type='BEGINS_WITH'):
        field = cvd_field_mapping[by]
        cvds = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.CollectionCvd_Query,
                collectionId=collection_id
            )
        return cvds


    def get_app_layers(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = layer_field_mapping[by]
        layers = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.AppLayer_Query
            )
        return layers


    def get_base_layers(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = layer_field_mapping[by]
        layers = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.BaseLayer_Query
            )
        return layers


    def get_collections(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = collection_field_mapping[by]
        collections = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Collection_Query
            )
        return collections


    def get_pending_devices(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = pending_device_field_mapping[by]
        pending_devices = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.PendingDevice_Query
            )
        return pending_devices


    def get_policies(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = policy_field_mapping[by]
        policies = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Policy_Query
            )
        return policies


    def get_volumes(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = volume_field_mapping[by]
        volumes = _collect_query_results(
                self,
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Volume_Query
            )
        return volumes
