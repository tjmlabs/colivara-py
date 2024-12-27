# EmbeddingsOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **List[object]** |  | 
**model** | **str** |  | 
**usage** | **object** |  | 

## Example

```python
from colivara_py.models.embeddings_out import EmbeddingsOut

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingsOut from a JSON string
embeddings_out_instance = EmbeddingsOut.from_json(json)
# print the JSON string representation of the object
print(EmbeddingsOut.to_json())

# convert the object into a dict
embeddings_out_dict = embeddings_out_instance.to_dict()
# create an instance of EmbeddingsOut from a dict
embeddings_out_from_dict = EmbeddingsOut.from_dict(embeddings_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


