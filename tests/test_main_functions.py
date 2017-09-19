from vmwaremirage import VmwareMirageClient
import config
import os


vm = VmwareMirageClient(server=config.server,
                        username=config.username,
                        password=os.environ['VMWARE_MIRAGE_PASSWORD'])


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
