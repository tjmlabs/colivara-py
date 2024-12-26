# colivara_py.HealthApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_health**](HealthApi.md#api_views_health) | **GET** /v1/health/ | Health


# **api_views_health**
> api_views_health()

Health

### Example


```python
import colivara_py
from colivara_py.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.colivara.com
# See configuration.py for a list of all supported configuration parameters.
configuration = colivara_py.Configuration(
    host = "https://api.colivara.com"
)


# Enter a context with an instance of the API client
with colivara_py.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = colivara_py.HealthApi(api_client)

    try:
        # Health
        api_instance.api_views_health()
    except Exception as e:
        print("Exception when calling HealthApi->api_views_health: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

