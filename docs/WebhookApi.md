# colivara_py.WebhookApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_add_webhook**](WebhookApi.md#api_views_add_webhook) | **POST** /v1/webhook/ | Add Webhook


# **api_views_add_webhook**
> WebhookOut api_views_add_webhook(webhook_in)

Add Webhook

Add a webhook to the service.  This endpoint allows the user to add a webhook to the service. The webhook will be called when a document is upserted with the upsertion status.  Events are document upsert successful, document upsert failed.  Args:     request: The HTTP request object, which includes the user information.     url (str): The URL of the webhook.  Returns:     A message indicating that the webhook was added successfully.  Raises:     HttpError: If the webhook is invalid.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.webhook_in import WebhookIn
from colivara_py.models.webhook_out import WebhookOut
from colivara_py.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.colivara.com
# See configuration.py for a list of all supported configuration parameters.
configuration = colivara_py.Configuration(
    host = "https://api.colivara.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: Bearer
configuration = colivara_py.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with colivara_py.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = colivara_py.WebhookApi(api_client)
    webhook_in = colivara_py.WebhookIn() # WebhookIn | 

    try:
        # Add Webhook
        api_response = api_instance.api_views_add_webhook(webhook_in)
        print("The response of WebhookApi->api_views_add_webhook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhookApi->api_views_add_webhook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webhook_in** | [**WebhookIn**](WebhookIn.md)|  | 

### Return type

[**WebhookOut**](WebhookOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

