# python-vmwaremirage
Python API for VMWare Mirage

This API is based on the brilliant zeep Python SOAP client. All this API provides is a wrapper for the zeep library, giving a set of convenience functions to perform common actions. To learn more about zeep, visit their [github](https://github.com/mvantellingen/python-zeep) or [documentation.](http://docs.python-zeep.org/en/master/)

To start with, instantiate an instance of the Mirage API:
```python
from vmwaremirage import VmwareMirageClient
import os

vm = VmwareMirageClient(server='mirageserver.example.com.au', username='svc-vmwaremirage', password=os.environ['VMWARE_MIRAGE_PASSWORD'])
```
