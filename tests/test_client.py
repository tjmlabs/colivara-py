
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


@responses.activate
def test_create_collection_invalid_name_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    error_detail = {"detail": "Collection name 'all' is not allowed."}
    
    responses.add(
        responses.POST,
        f"{base_url}/v1/collections/",
        json=error_detail,
        status=422
    )
    
    with pytest.raises(Exception) as exc_info:
        client.create_collection(name="all")
    assert "Value error, Collection name 'all' is not allowed." in str(exc_info.value)


@responses.activate
def test_get_collections_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    expected_out = [
        {
            "id": 1,
            "name": "test_collection",
            "metadata": {"description": "A test collection"}
        },
        {
            "id": 2,
            "name": "another_test_collection",
            "metadata": {"description": "Another test collection"}
        }
    ]
    
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/",
        json=expected_out,
        status=200
    )
    
    collections = client.list_collections()

    # Check that collections is a list
    assert isinstance(collections, list)
    assert len(collections) == 2

    # Check that each collection in the list is an instance of CollectionOut
    for collection in collections:
        assert isinstance(collection, CollectionOut)

    # Check the properties of the first collection in the list
    first_collection = collections[0]
    assert first_collection.id == 1
    assert first_collection.name == "test_collection"
    assert first_collection.metadata == {"description": "A test collection"}

    # Check the properties of the second collection in the list
    second_collection = collections[1]
    assert second_collection.id == 2
    assert second_collection.name == "another_test_collection"
    assert second_collection.metadata == {"description": "Another test collection"}


@responses.activate
def test_get_collections_empty_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    expected_out = []
    
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/",
        json=expected_out,
        status=200
    )
    
    collections = client.list_collections()

    # Check that collections is a list
    assert isinstance(collections, list)
    assert len(collections) == 0


@responses.activate
def test_get_collections_noauth_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)

    error_detail = {"detail": "Unauthorized"}
    
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/",
        json=error_detail,
        status=401
    )

    with pytest.raises(Exception) as exc_info:
        client.list_collections()
    assert "401 Client Error: Unauthorized for url:" in str(exc_info.value)


@responses.activate
def test_get_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    expected_out = {
        "id": 1,
        "name": "test_collection",
        "metadata": {"description": "A test collection"}
    }
    
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/test_collection/",
        json=expected_out,
        status=200
    )
    
    collection = client.get_collection(collection_name="test_collection")
    assert isinstance(collection, CollectionOut)
    assert collection.id == 1
    assert collection.name == "test_collection"
    assert collection.metadata == {"description": "A test collection"}

@responses.activate
def test_get_collection_not_found_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    error_detail = {"detail": "Collection 'test_collection' not found."}
    
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/test_collection/",
        json=error_detail,
        status=404
    )

    with pytest.raises(Exception) as exc_info:
        client.get_collection(collection_name="test_collection")
    assert "Collection 'test_collection' not found." in str(exc_info.value)


@responses.activate
def test_partial_update_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    expected_out = {
        "id": 1,
        "name": "updated_collection",
        "metadata": {"description": "An updated collection"}
    }
    
    responses.add(
        responses.PATCH,
        f"{base_url}/v1/collections/test_collection/",
        json=expected_out,
        status=200
    )
    
    collection = client.partial_update_collection(collection_name="test_collection", name="updated_collection", metadata={"description": "An updated collection"})
    assert isinstance(collection, CollectionOut)
    assert collection.id == 1
    assert collection.name == "updated_collection"
    assert collection.metadata == {"description": "An updated collection"}


@responses.activate
def test_partial_update_collection_not_found_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    error_detail = {"detail": "Collection 'test_collection' not found."}
    
    responses.add(
        responses.PATCH,
        f"{base_url}/v1/collections/test_collection/",
        json=error_detail,
        status=404
    )

    with pytest.raises(Exception) as exc_info:
        client.partial_update_collection(collection_name="test_collection", name="updated_collection", metadata={"description": "An updated collection"})
    assert "Collection 'test_collection' not found." in str(exc_info.value)


@responses.activate
def test_partial_update_collection_missing_params_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)

    with pytest.raises(Exception) as exc_info:
        client.partial_update_collection(collection_name="test_collection")
    assert "validation error for PatchCollectionIn\n  Value error, At least one field must be provided to update." in str(exc_info.value)


@responses.activate
def test_delete_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    responses.add(
        responses.DELETE,
        f"{base_url}/v1/collections/test_collection/",
        status=204
    )
    
    out = client.delete_collection(collection_name="test_collection")
    assert out is None


@responses.activate
def test_delete_collection_not_found_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = Colivara(base_url=base_url)
    
    error_detail = {"detail": "Collection 'test_collection' not found."}
    
    responses.add(
        responses.DELETE,
        f"{base_url}/v1/collections/test_collection/",
        json=error_detail,
        status=404
    )

    with pytest.raises(Exception) as exc_info:
        client.delete_collection(collection_name="test_collection")
    assert "Collection 'test_collection' not found." in str(exc_info.value)

