# CollectionOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**metadata** | **object** |  | 
**num_documents** | **int** |  | 

## Example

```python
from colivara_py.models.collection_out import CollectionOut

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionOut from a JSON string
collection_out_instance = CollectionOut.from_json(json)
# print the JSON string representation of the object
print(CollectionOut.to_json())

# convert the object into a dict
collection_out_dict = collection_out_instance.to_dict()
# create an instance of CollectionOut from a dict
collection_out_from_dict = CollectionOut.from_dict(collection_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


