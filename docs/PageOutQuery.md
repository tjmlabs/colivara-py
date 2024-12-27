# PageOutQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collection_name** | **str** |  | 
**collection_id** | **int** |  | 
**collection_metadata** | **object** |  | [optional] 
**document_name** | **str** |  | 
**document_id** | **int** |  | 
**document_metadata** | **object** |  | [optional] 
**page_number** | **int** |  | 
**raw_score** | **float** |  | 
**normalized_score** | **float** |  | 
**img_base64** | **str** |  | 

## Example

```python
from colivara_py.models.page_out_query import PageOutQuery

# TODO update the JSON string below
json = "{}"
# create an instance of PageOutQuery from a JSON string
page_out_query_instance = PageOutQuery.from_json(json)
# print the JSON string representation of the object
print(PageOutQuery.to_json())

# convert the object into a dict
page_out_query_dict = page_out_query_instance.to_dict()
# create an instance of PageOutQuery from a dict
page_out_query_from_dict = PageOutQuery.from_dict(page_out_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


