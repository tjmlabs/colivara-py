# QueryIn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** |  | 
**collection_name** | **str** |  | [optional] 
**top_k** | **int** |  | [optional] 
**query_filter** | [**QueryFilter**](QueryFilter.md) |  | [optional] 

## Example

```python
from colivara_py.models.query_in import QueryIn

# TODO update the JSON string below
json = "{}"
# create an instance of QueryIn from a JSON string
query_in_instance = QueryIn.from_json(json)
# print the JSON string representation of the object
print(QueryIn.to_json())

# convert the object into a dict
query_in_dict = query_in_instance.to_dict()
# create an instance of QueryIn from a dict
query_in_from_dict = QueryIn.from_dict(query_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


