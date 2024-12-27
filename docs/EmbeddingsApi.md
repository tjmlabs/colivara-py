# colivara_py.EmbeddingsApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_embeddings**](EmbeddingsApi.md#api_views_embeddings) | **POST** /v1/embeddings/ | Embeddings


# **api_views_embeddings**
> EmbeddingsOut api_views_embeddings(embeddings_in)

Embeddings

Embed a list of documents.  This endpoint allows the user to embed a list of documents.  Args:     request: The HTTP request object, which includes the user information.     payload (EmbeddingsIn): The input data for embedding the documents.  Returns:     EmbeddingsOut: The embeddings of the documents and metadata.  Raises:     HttpError: If the documents cannot be embedded.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.embeddings_in import EmbeddingsIn
from colivara_py.models.embeddings_out import EmbeddingsOut
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
    api_instance = colivara_py.EmbeddingsApi(api_client)
    embeddings_in = colivara_py.EmbeddingsIn() # EmbeddingsIn | 

    try:
        # Embeddings
        api_response = api_instance.api_views_embeddings(embeddings_in)
        print("The response of EmbeddingsApi->api_views_embeddings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmbeddingsApi->api_views_embeddings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **embeddings_in** | [**EmbeddingsIn**](EmbeddingsIn.md)|  | 

### Return type

[**EmbeddingsOut**](EmbeddingsOut.md)

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

