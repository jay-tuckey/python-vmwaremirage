# python-vmwaremirage
Python API for VMWare Mirage

This API is based on the brilliant zeep Python SOAP client. All this API provides is a wrapper for the zeep library, giving a set of convenience functions to perform common actions. To learn more about zeep, visit their [github](https://github.com/mvantellingen/python-zeep) or [documentation.](http://docs.python-zeep.org/en/master/)

To start with, instantiate an instance of the Mirage API:
```python
from vmwaremirage import VmwareMirageClient
import os

vm = VmwareMirageClient(server='mirageserver.example.com.au', username='svc-vmwaremirage', password=os.environ['VMWARE_MIRAGE_PASSWORD'])
```

Some of the available functions are:
```python
### CVDS ###
# Get all cvds (Warning, can take a while to fetch a large number)
cvds = vm.get_cvds()

# Get cvds with names starting with 'VM-'
cvds = vm.get_cvds(by="NAME", value="VM-", query_type="BEGINS_WITH")

# Get cvds used by a specific user
cvds = vm.get_cvds(by="USER_NAME", value="CDU-STAFF\\jtuckey", query_type="EQUALS")

# Get one specific cvd by ID (Note get_cvd not get_cvds)
cvd = vm.get_cvd(10025)

### Layers ###
# Get all app layers
apps = vm.get_app_layers()

# Get all versions of specific app layer
apps = vm.get_app_layers(by="ID", value=5, query_type="EQUALS") 

# Get all base layers
bases = vm.get_base_layers()

### Collections ###
# Get all collections
colls = vm.get_collections()

# Get all collections that contain "Alice Springs" in the description
colls = vm.get_collections(by="DESCRIPTION", value="Alice Springs", query_type="CONTAINS")

### Pending Devices ###
# Get all pending devices
pends = vm.get_pending_devices()

# Get all Windows 7 x64 pending devices
pends = vm.get_pending_devices(by="OS_VERSION", value="WIN7X64", query_type="EQUALS")

### Policies ###
# Get all policies
policies = vm.get_policies()

### Volumes ###
# Get all volumes
vols = vm.get_volumes()
```

There are more functions available through the VMware Mirage API that are not currently implemented through my API wrapper, but are availble directly through zeep. To get a summary of what's available, run `python -mzeep https://mirageserver.example.com.au:7443/mirageapi/MitService.svc?singleWsdl` and it will give you a summary of what's available. The full zeep client is available within the `VmwareMirageClient` object:
```python
>>> vm.client
<zeep.client.Client object at 0x7fa926365ef0>
```
