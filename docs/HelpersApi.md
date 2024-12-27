# colivara_py.HelpersApi

All URIs are relative to *https://api.colivara.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_views_file_to_base64**](HelpersApi.md#api_views_file_to_base64) | **POST** /v1/helpers/file-to-base64/ | File To Base64
[**api_views_file_to_imgbase64**](HelpersApi.md#api_views_file_to_imgbase64) | **POST** /v1/helpers/file-to-imgbase64/ | File To Imgbase64


# **api_views_file_to_base64**
> api_views_file_to_base64(file)

File To Base64

Upload one file, converts to base64 encoded strings.  Args:     request: The HTTP request object.     file UploadedFile): One uploaded file  Returns: str: base64 encoded string of the file.

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
    api_instance = colivara_py.HelpersApi(api_client)
    file = None # bytearray | 

    try:
        # File To Base64
        api_instance.api_views_file_to_base64(file)
    except Exception as e:
        print("Exception when calling HelpersApi->api_views_file_to_base64: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_views_file_to_imgbase64**
> List[FileOut] api_views_file_to_imgbase64(file)

File To Imgbase64

Upload one file, converts to images and return their base64 encoded strings with 1-indexed page numberss.  Args:     request: The HTTP request object.     file UploadedFile): One uploaded file  Returns:     List[FileOut]: A list of FileOut objects containing the base64 encoded strings of the images.

### Example

* Bearer Authentication (Bearer):

```python
import colivara_py
from colivara_py.models.file_out import FileOut
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
    api_instance = colivara_py.HelpersApi(api_client)
    file = None # bytearray | 

    try:
        # File To Imgbase64
        api_response = api_instance.api_views_file_to_imgbase64(file)
        print("The response of HelpersApi->api_views_file_to_imgbase64:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling HelpersApi->api_views_file_to_imgbase64: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**|  | 

### Return type

[**List[FileOut]**](FileOut.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

