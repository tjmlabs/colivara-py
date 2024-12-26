# colivara_py.FilterApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_filter**](FilterApi.md#api_views_filter) | **POST** /v1/filter/ | Filter


# **api_views_filter**
> Response api_views_filter(query_filter, expand=expand)

Filter

Filter for documents and collections that meet the criteria of the filter.  Args:     request: The HTTP request object, which includes the user information.     payload (QueryFilter): The input data for the filter, which includes the filter criteria.     expand (Optional[str]): A comma-separated list of fields to expand in the response. If \"pages\" is included, the document's pages will be included.  Returns:     DocumentOut: The retrieved documents with their details.     CollectionOut: The retrieved collections with their details.  Raises:     HttpError: If the collection does not exist or the query is invalid.  Example:     POST /filter/?expand=pages     {         \"on\": \"document\",         \"key\": \"breed\",         \"value\": \"collie\",         \"lookup\": \"contains\"     }

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.query_filter import QueryFilter
from colivara_py.models.response import Response
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
    api_instance = colivara_py.FilterApi(api_client)
    query_filter = colivara_py.QueryFilter() # QueryFilter | 
    expand = 'expand_example' # str |  (optional)

    try:
        # Filter
        api_response = api_instance.api_views_filter(query_filter, expand=expand)
        print("The response of FilterApi->api_views_filter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterApi->api_views_filter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_filter** | [**QueryFilter**](QueryFilter.md)|  | 
 **expand** | **str**|  | [optional] 

### Return type

[**Response**](Response.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**503** | Service Unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

