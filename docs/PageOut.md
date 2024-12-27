# PageOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_name** | **str** |  | [optional] 
**img_base64** | **str** |  | 
**page_number** | **int** |  | 

## Example

```python
from colivara_py.models.page_out import PageOut

# TODO update the JSON string below
json = "{}"
# create an instance of PageOut from a JSON string
page_out_instance = PageOut.from_json(json)
# print the JSON string representation of the object
print(PageOut.to_json())

# convert the object into a dict
page_out_dict = page_out_instance.to_dict()
# create an instance of PageOut from a dict
page_out_from_dict = PageOut.from_dict(page_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


