# WebhookIn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | 

## Example

```python
from colivara_py.models.webhook_in import WebhookIn

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookIn from a JSON string
webhook_in_instance = WebhookIn.from_json(json)
# print the JSON string representation of the object
print(WebhookIn.to_json())

# convert the object into a dict
webhook_in_dict = webhook_in_instance.to_dict()
# create an instance of WebhookIn from a dict
webhook_in_from_dict = WebhookIn.from_dict(webhook_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


