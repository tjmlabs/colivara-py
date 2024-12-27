# colivara_py.DocumentsApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_delete_document**](DocumentsApi.md#api_views_delete_document) | **DELETE** /v1/documents/delete-document/{document_name}/ | Delete Document
[**api_views_get_document**](DocumentsApi.md#api_views_get_document) | **GET** /v1/documents/{document_name}/ | Get Document
[**api_views_list_documents**](DocumentsApi.md#api_views_list_documents) | **GET** /v1/documents/ | List Documents
[**api_views_partial_update_document**](DocumentsApi.md#api_views_partial_update_document) | **PATCH** /v1/documents/{document_name}/ | Partial Update Document
[**api_views_upsert_document**](DocumentsApi.md#api_views_upsert_document) | **POST** /v1/documents/upsert-document/ | Upsert Document


# **api_views_delete_document**
> api_views_delete_document(document_name, collection_name=collection_name)

Delete Document

Delete a document by its Name.  This endpoint deletes a document specified by the `document_name` parameter. The document must belong to the authenticated user.  Args:     request: The HTTP request object, which includes authentication information.     collection_name (name): The name of the collection containing the document. Defaults to \"default_collection\". Use \"all\" to access all collections belonging to the user.     document_name (int): The name of the document to be deleted.  Returns:     dict: A message indicating that the document was deleted successfully.  Raises:     HTTPException: If the document does not exist or does not belong to the authenticated user.  Example:     DELETE /documents/delete-document/{document_name}/?collection_name={collection_name}

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
    api_instance = colivara_py.DocumentsApi(api_client)
    document_name = 'document_name_example' # str | 
    collection_name = 'collection_name_example' # str |  (optional)

    try:
        # Delete Document
        api_instance.api_views_delete_document(document_name, collection_name=collection_name)
    except Exception as e:
        print("Exception when calling DocumentsApi->api_views_delete_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_name** | **str**|  | 
 **collection_name** | **str**|  | [optional] 

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
**409** | Conflict |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_get_document**
> DocumentOut api_views_get_document(document_name, collection_name=collection_name, expand=expand)

Get Document

Retrieve a specific document from the user documents. Default collection is \"default_collection\". To get all documents, use collection_name=\"all\".  Args:     request: The HTTP request object.     document_name (str): The ID of the document to retrieve.     expand (Optional[str]): A comma-separated list of fields to expand in the response.                             If \"pages\" is included, the document's pages will be included.  Returns:     DocumentOut: The retrieved document with its details.  Raises:     HTTPException: If the document or collection is not found.  Example:     GET /documents/{document_name}/?collection_name={collection_name}&expand=pages

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.document_out import DocumentOut
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
    api_instance = colivara_py.DocumentsApi(api_client)
    document_name = 'document_name_example' # str | 
    collection_name = 'collection_name_example' # str |  (optional)
    expand = 'expand_example' # str |  (optional)

    try:
        # Get Document
        api_response = api_instance.api_views_get_document(document_name, collection_name=collection_name, expand=expand)
        print("The response of DocumentsApi->api_views_get_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->api_views_get_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_name** | **str**|  | 
 **collection_name** | **str**|  | [optional] 
 **expand** | **str**|  | [optional] 

### Return type

[**DocumentOut**](DocumentOut.md)

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
**409** | Conflict |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_list_documents**
> List[DocumentOut] api_views_list_documents(collection_name=collection_name, expand=expand)

List Documents

Fetch a list of documents for a given collection.  This endpoint retrieves documents associated with a specified collection name. Optionally, it can expand the response to include pages of each document.  Args:     request (Request): The request object.     collection_name (Optional[str]): The name of the collection to fetch documents from. Defaults to \"default_collection\". Use \"all\" to fetch documents from all collections.     expand (Optional[str]): A comma-separated string specifying additional fields to include in the response.                             If \"pages\" is included, the pages of each document will be included.  Returns:     List[DocumentOut]: A list of documents with their details. If expanded, includes pages of each document.  Raises:     HTTPException: If the collection or documents are not found.  Example:     GET /documents/?collection_name=default_collection&expand=pages

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.document_out import DocumentOut
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
    api_instance = colivara_py.DocumentsApi(api_client)
    collection_name = 'collection_name_example' # str |  (optional)
    expand = 'expand_example' # str |  (optional)

    try:
        # List Documents
        api_response = api_instance.api_views_list_documents(collection_name=collection_name, expand=expand)
        print("The response of DocumentsApi->api_views_list_documents:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->api_views_list_documents: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_name** | **str**|  | [optional] 
 **expand** | **str**|  | [optional] 

### Return type

[**List[DocumentOut]**](DocumentOut.md)

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

# **api_views_partial_update_document**
> DocumentOut api_views_partial_update_document(document_name, document_in_patch)

Partial Update Document

Partially update a document.  This endpoint allows for partial updates to a document's details. Only the fields provided in the payload will be updated. If the URL is changed or base64 is provided, the document will be re-embedded. Otherwise, only the metadata and name will be updated.  Args:     request: The request object containing authentication details.     document_name (str): The name of the document to be updated.     payload (DocumentInPatch): The payload containing the fields to be updated.  Returns:     Tuple[int, DocumentOut] | Tuple[int, GenericError]: A tuple containing the status code and the updated document or an error message.  Raises:     HTTPException: If the document is not found or the user is not authorized to update it.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.document_in_patch import DocumentInPatch
from colivara_py.models.document_out import DocumentOut
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
    api_instance = colivara_py.DocumentsApi(api_client)
    document_name = 'document_name_example' # str | 
    document_in_patch = colivara_py.DocumentInPatch() # DocumentInPatch | 

    try:
        # Partial Update Document
        api_response = api_instance.api_views_partial_update_document(document_name, document_in_patch)
        print("The response of DocumentsApi->api_views_partial_update_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->api_views_partial_update_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_name** | **str**|  | 
 **document_in_patch** | [**DocumentInPatch**](DocumentInPatch.md)|  | 

### Return type

[**DocumentOut**](DocumentOut.md)

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
**409** | Conflict |  -  |
**402** | Payment Required |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_upsert_document**
> DocumentOut api_views_upsert_document(document_in)

Upsert Document

Create or update a document in a collection. Average latency is 7 seconds per page.  This endpoint allows the user to create or update a document in a collection. The document can be provided as a URL or a base64-encoded string. if the collection is not provided, a collection named \"default_collection\" will be used. if the collection is provided, it will be created if it does not exist.  Args:     request: The HTTP request object, which includes the user information.     payload (DocumentIn): The input data for creating or updating the document.  Returns:     str: A message indicating that the document is being processed.  Raises:     HttpError: If the document cannot be created or updated.  Example:     POST /documents/upsert-document/     {         \"name\": \"my_document\",         \"metadata\": {\"author\": \"John Doe\"},         \"collection\": \"my_collection\",         \"url\": \"https://example.com/my_document.pdf,         \"wait\": true # optional, if true, the response will be sent after waiting for the document to be processed. Otherwise, it will be done asynchronously.     }

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.document_in import DocumentIn
from colivara_py.models.document_out import DocumentOut
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
    api_instance = colivara_py.DocumentsApi(api_client)
    document_in = colivara_py.DocumentIn() # DocumentIn | 

    try:
        # Upsert Document
        api_response = api_instance.api_views_upsert_document(document_in)
        print("The response of DocumentsApi->api_views_upsert_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocumentsApi->api_views_upsert_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_in** | [**DocumentIn**](DocumentIn.md)|  | 

### Return type

[**DocumentOut**](DocumentOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**202** | Accepted |  -  |
**400** | Bad Request |  -  |
**402** | Payment Required |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

