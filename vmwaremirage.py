from zeep import Client, xsd
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
import zeep.cache
import zeep.transports
from vmwaremirage_mappings import query_type_mapping, cvd_field_mapping, layer_field_mapping, collection_field_mapping, pending_device_field_mapping, policy_field_mapping, volume_field_mapping

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


    def query(self, field, value, page=1, query_type='BEGINS_WITH', get_definition=True):
        query_function = query_type_mapping[query_type]
        if field['type'] is 'String':
            query_filter = self.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(xsd.String(), value))
        elif field['type'] is 'Id':
            query_filter = self.query_factory[query_function](Field=field['name'], Value=self.type_factory.Id(value))
        elif field['type'] is 'Long':
            query_filter = self.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(xsd.Long(), value))
        elif field['type'] is 'Boolean':
            query_filter = self.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(xsd.Boolean(), value))
        else:
            raise Exception("Can't determine Value type")
        if get_definition:
            return self.query_factory.QueryDefinition(Filter=query_filter, Page=page)
        else:
            return query_filter


    def _collect_query_results(self, field, value, query_type, query_function, **kwargs):
        results = []
        current_page = 1
        while True:
            query = self.query(field=field, value=value, page=current_page, query_type=query_type)
            result = query_function(queryDefinition=query, **kwargs)
            # Drop out if there are no results
            if result['Elements'] is None:
                break
            results += result['Elements']['anyType']
            # Stop if on the last page
            if not result['NextPageAvailable']:
                break
            current_page += 1
        return results


    def get_cvds(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = cvd_field_mapping[by]
        cvds = self._collect_query_results(
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
        cvds = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.CollectionCvd_Query,
                collectionId=collection_id
            )
        return cvds


    def get_app_layers(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = layer_field_mapping[by]
        layers = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.AppLayer_Query
            )
        return layers


    def get_base_layers(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = layer_field_mapping[by]
        layers = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.BaseLayer_Query
            )
        return layers


    def get_collections(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = collection_field_mapping[by]
        collections = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Collection_Query
            )
        return collections


    def get_pending_devices(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = pending_device_field_mapping[by]
        pending_devices = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.PendingDevice_Query
            )
        return pending_devices


    def get_policies(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = policy_field_mapping[by]
        policies = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Policy_Query
            )
        return policies


    def get_volumes(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = volume_field_mapping[by]
        volumes = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Volume_Query
            )
        return volumes
