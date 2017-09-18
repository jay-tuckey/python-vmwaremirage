query_type_mapping = {
    'BEGINS_WITH': 'QueryFilterBeginsWith',
    'ENDS_WITH': 'QueryFilterEndsWith',
    'CONTAINS': 'QueryFilterContains',
    'EQUALS': 'QueryFilterEquals',
    'NOT_EQUALS': 'QueryFilterNotEquals'
}

cvd_field_mapping = {
    'ID': {
        'name': 'CVD_ID',
        'type': 'Id'
    },
    'DEVICE_ID': {
        'name': 'CVD_DEVICE_ID',
        'type': 'Id'
    },
    'POLICY_ID': {
        'name': 'CVD_POLICY_ID',
        'type': 'Id'
    },
    'NAME': {
        'name': 'CVD_NAME',
        'type': 'String'
    },
    'USER_NAME': {
        'name': 'CVD_USER_NAME',
        'type': 'String'
    },
    'POLICY_NAME': {
        'name': 'CVD_POLICY_NAME',
        'type': 'String'
    },
    'CONNECTION_STATE': {
        'name': 'CVD_DEVICE_CONNECTION_STATE',
        'type': 'Boolean'
    },
    'CLIENT_STATUS': {
        'name': 'CVD_DEVICE_CLIENT_STATUS',
        'type': 'String'
    },
    'PROGRESS': {
        'name': 'CVD_PROGRESS',
        'type': 'Long'
    },
    #TODO Work out how to query by machine version
    'MACHINE_VERSION': {
        'name': 'CVD_MACHINE_VERSION',
        'type': '?'
    },
}

layer_field_mapping = {
    'ID': {
        'name': 'BASE_IMAGE_LAYER_ID',
        'type': 'Id'
    },
    #TODO Work out how to query
    'TYPE': {
        'name': 'BASE_IMAGE_LAYER_TYPE',
        'type': '?'
    },
    'NAME': {
        'name': 'BASE_IMAGE_LAYER_NAME',
        'type': 'String'
    }
}

collection_field_mapping = {
    'ID': {
        'name': 'COLLECTION_ID',
        'type': 'Id'
    },
    'NAME': {
        'name': 'COLLECTION_NAME',
        'type': 'String'
    },
    'DESCRIPTION': {
        'name': 'COLLECTION_DESCRIPTION',
        'type': 'String'
    }
}

pending_device_field_mapping = {
    'ID': {
        'name': 'DEVICE_ID',
        'type': 'Id'
    },
    'NAME': {
        'name': 'DEVICE_NAME',
        'type': 'String'
    },
    'USER_NAME': {
        'name': 'DEVICE_USER_NAME',
        'type': 'String'
    },
    'MODEL_NAME': {
        'name': 'DEVICE_MODEL_NAME',
        'type': 'String'
    },
    'VENDOR_NAME': {
        'name': 'DEVICE_VENDOR_NAME',
        'type': 'String'
    },
    'OS_VERSION': {
        'name': 'DEVICE_OS_VERSION',
        'type': 'String'
    },
    'CONNECTION_STATE': {
        'name': 'DEVICE_CONNECTION_STATE',
        'type': 'Boolean'
    }
}

policy_field_mapping = {
    'ID': {
        'name': 'POLICY_ID',
        'type': 'Id'
    },
    'NAME': {
        'name': 'POLICY_NAME',
        'type': 'String'
    }
}

volume_field_mapping = {
    'ID': {
        'name': 'VOLUME_ID',
        'type': 'Id'
    },
    'NAME': {
        'name': 'VOLUME_NAME',
        'type': 'String'
    },
    'PATH': {
        'name': 'VOLUME_PATH',
        'type': 'String'
    }
}
