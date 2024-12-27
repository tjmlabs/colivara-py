# FileOut


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**img_base64** | **str** |  | 
**page_number** | **int** |  | 

## Example

```python
from colivara_py.models.file_out import FileOut

# TODO update the JSON string below
json = "{}"
# create an instance of FileOut from a JSON string
file_out_instance = FileOut.from_json(json)
# print the JSON string representation of the object
print(FileOut.to_json())

# convert the object into a dict
file_out_dict = file_out_instance.to_dict()
# create an instance of FileOut from a dict
file_out_from_dict = FileOut.from_dict(file_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


