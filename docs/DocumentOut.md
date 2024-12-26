# DocumentOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**metadata** | **object** |  | [optional] 
**url** | **str** |  | [optional] 
**num_pages** | **int** |  | 
**collection_name** | **str** |  | 
**pages** | [**List[PageOut]**](PageOut.md) |  | [optional] 

## Example

```python
from colivara_py.models.document_out import DocumentOut

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentOut from a JSON string
document_out_instance = DocumentOut.from_json(json)
# print the JSON string representation of the object
print(DocumentOut.to_json())

# convert the object into a dict
document_out_dict = document_out_instance.to_dict()
# create an instance of DocumentOut from a dict
document_out_from_dict = DocumentOut.from_dict(document_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


