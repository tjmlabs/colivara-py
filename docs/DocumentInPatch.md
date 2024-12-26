# DocumentInPatch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 
**collection_name** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**var_base64** | **str** |  | [optional] 
**use_proxy** | **bool** |  | [optional] 

## Example

```python
from colivara_py.models.document_in_patch import DocumentInPatch

# TODO update the JSON string below
json = "{}"
# create an instance of DocumentInPatch from a JSON string
document_in_patch_instance = DocumentInPatch.from_json(json)
# print the JSON string representation of the object
print(DocumentInPatch.to_json())

# convert the object into a dict
document_in_patch_dict = document_in_patch_instance.to_dict()
# create an instance of DocumentInPatch from a dict
document_in_patch_from_dict = DocumentInPatch.from_dict(document_in_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


