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


    def get_cvds(self, by='NAME', value='', query_type='BEGINS_WITH'):
        field = self.cvd_field_mapping[by]
        cvds = []
        current_page = 1
        while True:
            query = self.query(field=field, value=value, page=current_page, query_type=query_type)
            result = self.client.service.Cvd_Query(queryDefinition=query)
            # Drop out if there are no results
            if result['Elements'] is None:
                break
            cvds += result['Elements']['anyType']
            # Stop if on the last page
            if not result['NextPageAvailable']:
                break
            current_page += 1
        return cvds
