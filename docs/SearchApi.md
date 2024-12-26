# colivara_py.SearchApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_search**](SearchApi.md#api_views_search) | **POST** /v1/search/ | Search


# **api_views_search**
> QueryOut api_views_search(query_in)

Search

Search for pages similar to a given query.  This endpoint allows the user to search for pages similar to a given query. The search is performed across all documents in the specified collection.  Args:     request: The HTTP request object, which includes the user information.     payload (QueryIn): The input data for the search, which includes the query string and collection ID.  Returns:     QueryOut: The search results, including the query and a list of similar pages.  Raises:     HttpError: If the collection does not exist or the query is invalid.  Example:     POST /search/     {         \"query\": \"dog\",         \"collection_name\": \"my_collection\",         \"top_k\": 3,         \"query_filter\": {             \"on\": \"document\",             \"key\": \"breed\",             \"value\": \"collie\",             \"lookup\": \"contains\"         }     }

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.query_in import QueryIn
from colivara_py.models.query_out import QueryOut
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
    api_instance = colivara_py.SearchApi(api_client)
    query_in = colivara_py.QueryIn() # QueryIn | 

    try:
        # Search
        api_response = api_instance.api_views_search(query_in)
        print("The response of SearchApi->api_views_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->api_views_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_in** | [**QueryIn**](QueryIn.md)|  | 

### Return type

[**QueryOut**](QueryOut.md)

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
**402** | Payment Required |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

