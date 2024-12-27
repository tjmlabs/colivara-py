# colivara_py.CollectionsApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_create_collection**](CollectionsApi.md#api_views_create_collection) | **POST** /v1/collections/ | Create Collection
[**api_views_delete_collection**](CollectionsApi.md#api_views_delete_collection) | **DELETE** /v1/collections/{collection_name}/ | Delete Collection
[**api_views_get_collection**](CollectionsApi.md#api_views_get_collection) | **GET** /v1/collections/{collection_name}/ | Get Collection
[**api_views_list_collections**](CollectionsApi.md#api_views_list_collections) | **GET** /v1/collections/ | List Collections
[**api_views_partial_update_collection**](CollectionsApi.md#api_views_partial_update_collection) | **PATCH** /v1/collections/{collection_name}/ | Partial Update Collection


# **api_views_create_collection**
> CollectionOut api_views_create_collection(collection_in)

Create Collection

Create a new collection.  This endpoint allows the user to create a new collection with the specified name and metadata.  Args:     request: The HTTP request object, which includes the user information.     payload (CollectionIn): The input data for creating the collection, which includes the name and metadata.  Returns:     dict: A dictionary containing the ID of the newly created collection and a success message.  Raises:     HttpError: If the user already has a collection with the same name.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.collection_in import CollectionIn
from colivara_py.models.collection_out import CollectionOut
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
    api_instance = colivara_py.CollectionsApi(api_client)
    collection_in = colivara_py.CollectionIn() # CollectionIn | 

    try:
        # Create Collection
        api_response = api_instance.api_views_create_collection(collection_in)
        print("The response of CollectionsApi->api_views_create_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->api_views_create_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_in** | [**CollectionIn**](CollectionIn.md)|  | 

### Return type

[**CollectionOut**](CollectionOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**409** | Conflict |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_delete_collection**
> api_views_delete_collection(collection_name)

Delete Collection

Delete a collection by its name.  This endpoint deletes a collection specified by the `collection_name` parameter. The collection must belong to the authenticated user.  Args:     request: The HTTP request object, which includes authentication information.     collection_id (int): The ID of the collection to be deleted.  Returns:     dict: A message indicating that the collection was deleted successfully.  Raises:     HTTPException: If the collection does not exist or does not belong to the authenticated user.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
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
    api_instance = colivara_py.CollectionsApi(api_client)
    collection_name = 'collection_name_example' # str | 

    try:
        # Delete Collection
        api_instance.api_views_delete_collection(collection_name)
    except Exception as e:
        print("Exception when calling CollectionsApi->api_views_delete_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_get_collection**
> CollectionOut api_views_get_collection(collection_name)

Get Collection

Retrieve a collection by its name.  Args:     request: The request object containing authentication information.     collection_name (str): The name of the collection to retrieve.  Returns:     CollectionOut: The retrieved collection with its ID, name, and metadata.  Raises:     HTTPException: If the collection is not found or the user is not authorized to access it.  Endpoint:     GET /collections/{collection_name}  Tags:     collections  Authentication:     Bearer token required.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.collection_out import CollectionOut
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
    api_instance = colivara_py.CollectionsApi(api_client)
    collection_name = 'collection_name_example' # str | 

    try:
        # Get Collection
        api_response = api_instance.api_views_get_collection(collection_name)
        print("The response of CollectionsApi->api_views_get_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->api_views_get_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_name** | **str**|  | 

### Return type

[**CollectionOut**](CollectionOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_list_collections**
> List[CollectionOut] api_views_list_collections()

List Collections

Endpoint to list collections.  This endpoint retrieves a list of collections owned by the authenticated user.  Args:     request: The request object containing authentication information.  Returns:     A list of CollectionOut objects representing the collections owned by the authenticated user.  Raises:     HTTPException: If there is an issue with the request or authentication.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.collection_out import CollectionOut
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
    api_instance = colivara_py.CollectionsApi(api_client)

    try:
        # List Collections
        api_response = api_instance.api_views_list_collections()
        print("The response of CollectionsApi->api_views_list_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->api_views_list_collections: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[CollectionOut]**](CollectionOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_partial_update_collection**
> CollectionOut api_views_partial_update_collection(collection_name, patch_collection_in)

Partial Update Collection

Partially update a collection.  This endpoint allows for partial updates to a collection's details. Only the fields provided in the payload will be updated.  Args:     request: The request object containing authentication details.     collection_name (str): The name of the collection to be updated.     payload (PatchCollectionIn): The payload containing the fields to be updated.  Returns:     dict: A message indicating the collection was updated successfully.  Raises:     HTTPException: If the collection is not found or the user is not authorized to update it.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.collection_out import CollectionOut
from colivara_py.models.patch_collection_in import PatchCollectionIn
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
    api_instance = colivara_py.CollectionsApi(api_client)
    collection_name = 'collection_name_example' # str | 
    patch_collection_in = colivara_py.PatchCollectionIn() # PatchCollectionIn | 

    try:
        # Partial Update Collection
        api_response = api_instance.api_views_partial_update_collection(collection_name, patch_collection_in)
        print("The response of CollectionsApi->api_views_partial_update_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->api_views_partial_update_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_name** | **str**|  | 
 **patch_collection_in** | [**PatchCollectionIn**](PatchCollectionIn.md)|  | 

### Return type

[**CollectionOut**](CollectionOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

