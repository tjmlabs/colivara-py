# DocumentIn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**metadata** | **object** |  | [optional] 
**collection_name** | **str** | The name of the collection to which the document belongs. If not provided, the document will be added to the default_collection. Use &#39;all&#39; to access all collections belonging to the user. | [optional] [default to 'default_collection']
**url** | **str** |  | [optional] 
**var_base64** | **str** |  | [optional] 
**wait** | **bool** |  | [optional] 
**use_proxy** | **bool** |  | [optional] 

## Example

```python
from colivara_py.models.document_in import DocumentIn

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentIn from a JSON string
document_in_instance = DocumentIn.from_json(json)
# print the JSON string representation of the object
print(DocumentIn.to_json())

# convert the object into a dict
document_in_dict = document_in_instance.to_dict()
# create an instance of DocumentIn from a dict
document_in_from_dict = DocumentIn.from_dict(document_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


