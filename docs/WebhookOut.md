# WebhookOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app_id** | **str** |  | 
**endpoint_id** | **str** |  | 
**webhook_secret** | **str** |  | 

## Example

```python
from colivara_py.models.webhook_out import WebhookOut

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookOut from a JSON string
webhook_out_instance = WebhookOut.from_json(json)
# print the JSON string representation of the object
print(WebhookOut.to_json())

# convert the object into a dict
webhook_out_dict = webhook_out_instance.to_dict()
# create an instance of WebhookOut from a dict
webhook_out_from_dict = WebhookOut.from_dict(webhook_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


