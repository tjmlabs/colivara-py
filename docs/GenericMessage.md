# GenericMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**detail** | **str** |  | 

## Example

```python
from colivara_py.models.generic_message import GenericMessage

# TODO update the JSON string below
json = "{}"
# create an instance of GenericMessage from a JSON string
generic_message_instance = GenericMessage.from_json(json)
# print the JSON string representation of the object
print(GenericMessage.to_json())

# convert the object into a dict
generic_message_dict = generic_message_instance.to_dict()
# create an instance of GenericMessage from a dict
generic_message_from_dict = GenericMessage.from_dict(generic_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


