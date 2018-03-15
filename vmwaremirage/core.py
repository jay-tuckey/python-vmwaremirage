from zeep import Client, xsd
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
import zeep.cache
import zeep.transports
from .mappings import query_type_mapping, cvd_field_mapping, layer_field_mapping, collection_field_mapping, pending_device_field_mapping, policy_field_mapping, volume_field_mapping
from .queries import _collect_query_results
from collections import namedtuple

class VmwareMirageClient():
    def __init__(self, server, username, password, port=7443, cache=zeep.cache.InMemoryCache()):
        transport = zeep.transports.Transport(cache=cache)
        self.history = HistoryPlugin()
        self.client = Client("https://{}:{}/mirageapi/MitService.svc?singleWsdl".format(server, port), plugins=[self.history], transport=transport)

        self.username = username
        self.password = password

        login_response = self.client.service.Login(username=username, password=password)


        self.query_factory = self.client.type_factory('vmware.mirage.mit.query')
        self.type_factory = self.client.type_factory('vmware.mirage.mit.types')


    def reauth(function):
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except Fault as e:
                if e.message == 'The session is not authenticated.':
                    login_response = self.client.service.Login(username=self.username, password=self.password)
                    return function(self, *args, **kwargs)
                else:
                    raise(e)
        return wrapper


    @reauth
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


    @reauth
    def get_cvd(self, id):
        result = self.client.service.Cvd_Get(id=id)
        return result


    @reauth
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


    @reauth
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


    @reauth
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


    @reauth
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


    @reauth
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


    @reauth
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


    @reauth
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



    @reauth
    def provision_pending_device(self, pending_device_id, policy, base_layer, app_layers, identity_info, volume_id, ignore_warnings=False):
        pending_device = self.type_factory.ArrayOfId([self.type_factory.Id(pending_device_id)])

        _policy = self.type_factory.ImageId(
            self.type_factory.Id(policy.id),
            self.type_factory.ImageVersion(policy.major_version, policy.minor_version)
            )

        _base_layer = self.type_factory.ImageId(
            self.type_factory.Id(base_layer.id),
            self.type_factory.ImageVersion(base_layer.major_version, base_layer.minor_version)
            )

        app_layers_list = [
            self.type_factory.ImageId(
                self.type_factory.Id(app.id),
                self.type_factory.ImageVersion(app.major_version, app.minor_version)
                )
            for app in app_layers
            ]

        app_layers_array = self.type_factory.ArrayOfImageId(app_layers_list)

        _identity_info = self.type_factory.MachineIdentityInfo(
            DomainMember=identity_info.domain_member,
            DomainOrWorkgroupName=identity_info.domain_or_workgroup_name,
            MachineName=identity_info.new_machine_name,
            OU=identity_info.ou,
            Password=identity_info.password,
            User=identity_info.user
            )

        _volume_id = self.type_factory.Id(volume_id)

        return self.client.service.PendingDevice_Provision(
            pendingDevices=pending_device,
            policyImageId=_policy,
            baseLayerImageId=_base_layer,
            appLayerImageIds=app_layers_array,
            identityInfo=_identity_info,
            volumeId=_volume_id,
            ignoreWarnings=ignore_warnings
            )


    Policy = namedtuple('Policy', ['id', 'major_version', 'minor_version'])
    AppLayer = namedtuple('AppLayer', ['id', 'major_version', 'minor_version'])
    BaseLayer = namedtuple('BaseLayer', ['id', 'major_version', 'minor_version'])
    IdentityInfo = namedtuple('IdentityInfo', ['domain_member', 'domain_or_workgroup_name', 'new_machine_name', 'ou', 'password', 'user'])
