from zeep import Client, xsd
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
import zeep.cache
import zeep.transports

class VmwareMirageClient():
    cvd_field_mapping = {
        'ID': 'CVD_ID',
        'DEVICE_ID': 'CVD_DEVICE_ID',
        'POLICY_ID': 'CVD_POLICY_ID',
        'NAME': 'CVD_NAME',
        'USER_NAME': 'CVD_USER_NAME',
        'POLICY_NAME': 'CVD_POLICY_NAME',
        'CONNECTION_STATE': 'CVD_DEVICE_CONNECTION_STATE',
        'CLIENT_STATUS': 'CVD_DEVICE_CLIENT_STATUS',
        'PROGRESS': 'CVD_PROGRESS',
        'MACHINE_VERSION': 'CVD_MACHINE_VERSION'
    }

    query_type_mapping = {
        'BEGINS_WITH': 'QueryFilterBeginsWith',
        'ENDS_WITH': 'QueryFilterEndsWith',
        'CONTAINS': 'QueryFilterContains',
        'EQUALS': 'QueryFilterEquals',
        'NOT_EQUALS': 'QueryFilterNotEquals'
    }

    layer_field_mapping = {
        'ID': 'BASE_IMAGE_LAYER_ID',
        'TYPE': 'BASE_IMAGE_LAYER_TYPE',
        'NAME': 'BASE_IMAGE_LAYER_NAME'
    }

    collection_field_mapping = {
        'ID': 'COLLECTION_ID',
        'NAME': 'COLLECTION_NAME',
        'DESCRIPTION': 'COLLECTION_DESCRIPTION'
    }

    pending_device_field_mapping = {
        'ID': 'DEVICE_ID',
        'NAME': 'DEVICE_NAME',
        'USER_NAME': 'DEVICE_USER_NAME',
        'MODEL_NAME': 'DEVICE_MODEL_NAME',
        'VENDOR_NAME': 'DEVICE_VENDOR_NAME',
        'OS_VERSION': 'DEVICE_OS_VERSION',
        'CONNECTION_STATE': 'DEVICE_CONNECTION_STATE'
    }

    policy_field_mapping = {
        'ID': 'POLICY_ID',
        'NAME': 'POLICY_NAME'
    }

    volume_field_mapping = {
        'ID': 'VOLUME_ID',
        'NAME': 'VOLUME_NAME',
        'PATH': 'VOLUME_PATH'
    }

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
        query_function = self.query_type_mapping[query_type]
        query_filter = self.query_factory[query_function](Field=field, Value=xsd.AnyObject(xsd.String(), value))
        if get_definition:
            return(self.query_factory.QueryDefinition(Filter=query_filter, Page=page))
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
        field = self.cvd_field_mapping[by]
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
        field = self.cvd_field_mapping[by]
        cvds = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.CollectionCvd_Query,
                collectionId=collection_id
            )
        return cvds


    def get_app_layers(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.layer_field_mapping[by]
        layers = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.AppLayer_Query
            )
        return layers


    def get_base_layers(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.layer_field_mapping[by]
        layers = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.BaseLayer_Query
            )
        return layers


    def get_collections(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.collection_field_mapping[by]
        collections = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Collection_Query
            )
        return collections


    def get_pending_devices(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.pending_device_field_mapping[by]
        pending_devices = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.PendingDevice_Query
            )
        return pending_devices


    def get_policies(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.policy_field_mapping[by]
        policies = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Policy_Query
            )
        return policies

    
    def get_volumes(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.volume_field_mapping[by]
        volumes = self._collect_query_results(
                field=field,
                value=value,
                query_type=query_type,
                query_function=self.client.service.Volume_Query
            )
        return volumes
