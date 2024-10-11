
import os
import pytest
from colivara_py import Colivara
from colivara_py.models import CollectionOut
import responses

@pytest.fixture
def api_key():
    return "test_api_key"

@responses.activate
def test_create_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    expected_out = {
        "id": 1,
        "name": "test_collection",
        "metadata": {"description": "A test collection"}
    }
    
    responses.add(
        responses.POST,
        f"{base_url}/v1/collections/",
        json=expected_out,
        status=201
    )
    
    collection = client.create_collection(name="test_collection", metadata={"description": "A test collection"})
    assert isinstance(collection, CollectionOut)
    assert collection.id == 1
    assert collection.name == "test_collection"
    assert collection.metadata == {"description": "A test collection"}

@responses.activate
def test_create_collection_conflict_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    error_detail = {"detail": "Collection already exists."}
    
    responses.add(
        responses.POST,
        f"{base_url}/v1/collections/",
        json=error_detail,
        status=409
    )
    
    with pytest.raises(Exception) as exc_info:
        client.create_collection(name="existing_collection")
    assert "Conflict error: Collection already exists." in str(exc_info.value)

