from vmwaremirage import VmwareMirageClient
import config
import config_secure
import os


vm = VmwareMirageClient(server=config_secure.server,
                        username=config_secure.username,
                        password=os.environ['VMWARE_MIRAGE_PASSWORD'])


def test_reauth():
    # Cofirm we are working
    cvd = vm.get_cvd(config.cvd_1['id'])
    assert cvd.Name == config.cvd_1['name']

    # Logout
    vm.client.service.Logout()

    # And try again. It should automatically re-authenticate
    cvd = vm.get_cvd(config.cvd_1['id'])
    assert cvd.Name == config.cvd_1['name']


def test_get_cvds():
    # Test the by id function
    cvd = vm.get_cvd(config.cvd_1['id'])
    assert cvd.Name == config.cvd_1['name']

    # Test getting two cvds by id
    cvds = vm.get_cvds(by='ID', value=[config.cvd_1['id'],config.cvd_2['id']], query_type='EQUALS')
    assert len(cvds) == 2

    cvds = vm.get_cvds(by='DEVICE_ID', value=[config.cvd_1['deviceid'],config.cvd_2['deviceid']], query_type='EQUALS')
    assert len(cvds) == 2

    cvds = vm.get_cvds(by='POLICY_ID', value=config.cvd_1['policyid'], query_type='EQUALS')
    assert len(cvds) >= 1

    cvds = vm.get_cvds(by='NAME', value=config.cvd_1['name'])
    assert len(cvds) == 1

    cvds = vm.get_cvds(by='USER_NAME', value=config.cvd_1['username'], query_type='CONTAINS')
    assert len(cvds) >= 1

    cvds = vm.get_cvds(by='POLICY_NAME', value=config.cvd_1['policyname'], query_type='ENDS_WITH')
    assert len(cvds) >= 1

    cvds = vm.get_cvds(by='CONNECTION_STATE', value=False, query_type='EQUALS')
    assert len(cvds) >= 1

    cvds = vm.get_cvds(by='CLIENT_STATUS', value='Idle', query_type='EQUALS')
    assert len(cvds) >= 1

    cvds = vm.get_cvds(by='PROGRESS', value=100, query_type='NOT_EQUALS')
    assert len(cvds) >= 1


def test_get_collection_cvds():
    cvds = vm.get_collection_cvds(config.collection['id'])
    assert len(cvds) >= 1


def test_get_app_layers():
    layers = vm.get_app_layers()
    assert len(layers) >= 1

    layer = vm.get_app_layers(by='ID', value=config.app_layer['id'], query_type='EQUALS')[0]
    assert layer.Name == config.app_layer['name']

    layers = vm.get_app_layers(by='NAME', value=config.app_layer['name'])
    assert len(layers) >= 1


def test_get_base_layers():
    layers = vm.get_base_layers()
    assert len(layers) >= 1

    layer = vm.get_base_layers(by='ID', value=config.base_layer['id'], query_type='EQUALS')[0]
    assert layer.Name == config.base_layer['name']

    layers = vm.get_base_layers(by='NAME', value=config.base_layer['name'])
    assert len(layers) >= 1


def test_get_collections():
    colls = vm.get_collections(by='ID', value=config.collection['id'], query_type='EQUALS')
    assert len(colls) == 1

    colls = vm.get_collections(by='NAME', value=config.collection['name'])
    assert len(colls) >= 1

    colls = vm.get_collections(by='DESCRIPTION', value=config.collection['description'], query_type='CONTAINS')
    assert len(colls) >= 1


def test_get_pending_devices():
    pends = vm.get_pending_devices(by='DEVICE_ID', value=config.pending['deviceid'], query_type='EQUALS')
    assert len(pends) == 1

    pends = vm.get_pending_devices(by='NAME', value=config.pending['name'])
    assert len(pends) == 1

    pends = vm.get_pending_devices(by='USER_NAME', value=config.pending['username'], query_type='CONTAINS')
    assert len(pends) >= 1

    pends = vm.get_pending_devices(by='CONNECTION_STATE', value=False, query_type='EQUALS')
    assert len(pends) >= 1

    pends = vm.get_pending_devices(by='MODEL_NAME', value=config.pending['model'], query_type='EQUALS')
    assert len(pends) >= 1

    pends = vm.get_pending_devices(by='VENDOR_NAME', value=config.pending['vendor'], query_type='EQUALS')
    assert len(pends) >= 1

    pends = vm.get_pending_devices(by='OS_VERSION', value=config.pending['os'], query_type='EQUALS')
    assert len(pends) >= 1


def test_get_policies():
    pols = vm.get_policies(by='ID', value=config.policy['id'], query_type='EQUALS')
    assert len(pols) == 1

    pols = vm.get_policies(by='NAME', value=config.policy['name'], query_type='EQUALS')
    assert len(pols) == 1


def test_get_volumes():
    vols = vm.get_volumes(by='ID', value=config.volume['id'], query_type='EQUALS')
    assert len(vols) == 1

    vols = vm.get_volumes(by='NAME', value=config.volume['name'], query_type='EQUALS')
    assert len(vols) == 1

    vols = vm.get_volumes(by='PATH', value=config.volume['path'], query_type='EQUALS')
