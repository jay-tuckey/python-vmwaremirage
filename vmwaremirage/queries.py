from .mappings import query_type_mapping


def query_filter(vm, field, value, query_type):
    query_function = query_type_mapping[query_type]
    if field['type'] is 'String':
        query_filter = vm.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(xsd.String(), value))
    elif field['type'] is 'Id':
        query_filter = vm.query_factory[query_function](Field=field['name'], Value=vm.type_factory.Id(value))
    elif field['type'] is 'Long':
        query_filter = vm.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(xsd.Long(), value))
    elif field['type'] is 'Boolean':
        query_filter = vm.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(xsd.Boolean(), value))
    elif field['type'] is 'OsVersion':
        query_filter = vm.query_factory[query_function](Field=field['name'], Value=xsd.AnyObject(vm.query_factory.OsVersion, value))
    else:
        raise Exception("Can't determine Value type")
    return query_filter


def multi_query(vm, filters, join_type):
    query_array = vm.query_factory.ArrayOfQueryFilter(QueryFilter=filters)
    if join_type is 'OR':
        multi_filter = vm.query_factory.QueryFilterOr(Filters=query_array)
    elif join_type is 'AND':
        multi_filter = vm.query_factory.QueryFilterAnd(Filters=query_array)
    else:
        raise Exception('join_type must be either OR or AND')
    return multi_filter

def query(vm, field, value, page=1, query_type='BEGINS_WITH'):
    if isinstance(value, list):
        filters = [query_filter(vm, field=field, value=item, query_type=query_type) for item in value]
        q_filter = multi_query(vm, filters, 'OR')
    else:
        q_filter = query_filter(field=field, value=value, query_type=query_type)
    return vm.query_factory.QueryDefinition(Filter=q_filter, Page=page)


def _collect_query_results(vm, field, value, query_type, query_function, **kwargs):
    results = []
    current_page = 1
    while True:
        query_definition = query(vm, field=field, value=value, page=current_page, query_type=query_type)
        result = query_function(queryDefinition=query_definition, **kwargs)
        # Drop out if there are no results
        if result['Elements'] is None:
            break
        results += result['Elements']['anyType']
        # Stop if on the last page
        if not result['NextPageAvailable']:
            break
        current_page += 1
    return results
