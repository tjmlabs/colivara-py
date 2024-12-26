# EmbeddingsIn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input_data** | **List[str]** |  | 
**task** | [**TaskEnum**](TaskEnum.md) |  | 

## Example

```python
from colivara_py.models.embeddings_in import EmbeddingsIn

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingsIn from a JSON string
embeddings_in_instance = EmbeddingsIn.from_json(json)
# print the JSON string representation of the object
print(EmbeddingsIn.to_json())

# convert the object into a dict
embeddings_in_dict = embeddings_in_instance.to_dict()
# create an instance of EmbeddingsIn from a dict
embeddings_in_from_dict = EmbeddingsIn.from_dict(embeddings_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


