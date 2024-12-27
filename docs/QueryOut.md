# QueryOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** |  | 
**results** | [**List[PageOutQuery]**](PageOutQuery.md) |  | 

## Example

```python
from colivara_py.models.query_out import QueryOut

# TODO update the JSON string below
json = "{}"
# create an instance of QueryOut from a JSON string
query_out_instance = QueryOut.from_json(json)
# print the JSON string representation of the object
print(QueryOut.to_json())

# convert the object into a dict
query_out_dict = query_out_instance.to_dict()
# create an instance of QueryOut from a dict
query_out_from_dict = QueryOut.from_dict(query_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


