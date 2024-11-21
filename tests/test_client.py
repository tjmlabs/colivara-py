import base64
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import responses
from pydantic import ValidationError
from requests.exceptions import HTTPError

from colivara_py import AsyncColiVara, ColiVara
from colivara_py.models import (
    CollectionOut,
    DocumentIn,
    DocumentInPatch,
    DocumentOut,
    EmbeddingsOut,
    FileOut,
    GenericMessage,
    PageOutQuery,
    PatchCollectionIn,
    QueryFilter,
    QueryOut,
    WebhookOut,
)


def test_colivara_init_no_api_key():
    with pytest.raises(
        ValueError,
        match="API key must be provided either through parameter or COLIVARA_API_KEY environment variable.",
    ):
        ColiVara(base_url="https://api.test.com")


@pytest.fixture
def api_key():
    return "test_api_key"


@responses.activate
def test_create_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "id": 1,
        "name": "test_collection",
        "metadata": {"description": "A test collection"},
        "num_documents": 0,
    }

    responses.add(
        responses.POST, f"{base_url}/v1/collections/", json=expected_out, status=201
    )

    collection = client.create_collection(
        name="test_collection", metadata={"description": "A test collection"}
    )
    assert isinstance(collection, CollectionOut)
    assert collection.id == 1
    assert collection.name == "test_collection"
    assert collection.metadata == {"description": "A test collection"}
    assert collection.num_documents == 0


@responses.activate
def test_create_collection_conflict_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_detail = {"detail": "Collection already exists."}

    responses.add(
        responses.POST, f"{base_url}/v1/collections/", json=error_detail, status=409
    )

    with pytest.raises(Exception) as exc_info:
        client.create_collection(name="existing_collection")
    assert "Conflict error: Collection already exists." in str(exc_info.value)


@responses.activate
def test_create_collection_unexpected_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # Simulate an unexpected error (e.g., 500 Internal Server Error)
    responses.add(
        responses.POST,
        f"{base_url}/v1/collections/",
        json={"error": "Internal Server Error"},
        status=500,
    )

    with pytest.raises(HTTPError):
        client.create_collection(name="test_collection")


@responses.activate
def test_create_collection_invalid_name_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_detail = {"detail": "Collection name 'all' is not allowed."}

    responses.add(
        responses.POST, f"{base_url}/v1/collections/", json=error_detail, status=422
    )

    with pytest.raises(Exception) as exc_info:
        client.create_collection(name="all")
    assert "Value error, Collection name 'all' is not allowed." in str(exc_info.value)


@responses.activate
def test_get_collections_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = [
        {
            "id": 1,
            "name": "test_collection",
            "metadata": {"description": "A test collection"},
            "num_documents": 2,
        },
        {
            "id": 2,
            "name": "another_test_collection",
            "metadata": {"description": "Another test collection"},
            "num_documents": 3,
        },
    ]

    responses.add(
        responses.GET, f"{base_url}/v1/collections/", json=expected_out, status=200
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
    assert first_collection.num_documents == 2

    # Check the properties of the second collection in the list
    second_collection = collections[1]
    assert second_collection.id == 2
    assert second_collection.name == "another_test_collection"
    assert second_collection.metadata == {"description": "Another test collection"}
    assert second_collection.num_documents == 3


@responses.activate
def test_list_collections_unexpected_format(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # Simulate an unexpected response format
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/",
        json={"unexpected": "format"},
        status=200,
    )

    with pytest.raises(ValueError, match="Unexpected response format"):
        client.list_collections()


@responses.activate
def test_list_collections_unexpected_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # Simulate an unexpected error (e.g., 500 Internal Server Error)
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/",
        json={"error": "Internal Server Error"},
        status=500,
    )

    with pytest.raises(HTTPError):
        client.list_collections()


@responses.activate
def test_get_collections_empty_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = []

    responses.add(
        responses.GET, f"{base_url}/v1/collections/", json=expected_out, status=200
    )

    collections = client.list_collections()

    # Check that collections is a list
    assert isinstance(collections, list)
    assert len(collections) == 0


@responses.activate
def test_get_collections_noauth_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_detail = {"detail": "Unauthorized"}

    responses.add(
        responses.GET, f"{base_url}/v1/collections/", json=error_detail, status=401
    )

    with pytest.raises(Exception) as exc_info:
        client.list_collections()
    assert "401 Client Error: Unauthorized for url:" in str(exc_info.value)


@responses.activate
def test_get_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "id": 1,
        "name": "test_collection",
        "metadata": {"description": "A test collection"},
        "num_documents": 2,
    }

    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/test_collection/",
        json=expected_out,
        status=200,
    )

    collection = client.get_collection(collection_name="test_collection")
    assert isinstance(collection, CollectionOut)
    assert collection.id == 1
    assert collection.name == "test_collection"
    assert collection.metadata == {"description": "A test collection"}
    assert collection.num_documents == 2


@responses.activate
def test_get_collection_not_found_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_detail = {"detail": "Collection 'test_collection' not found."}

    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/test_collection/",
        json=error_detail,
        status=404,
    )

    with pytest.raises(Exception) as exc_info:
        client.get_collection(collection_name="test_collection")
    assert "Collection 'test_collection' not found." in str(exc_info.value)


@responses.activate
def test_get_collection_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.GET,
        f"{base_url}/v1/collections/test_collection/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.get_collection(collection_name="test_collection")


@responses.activate
def test_partial_update_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "id": 1,
        "name": "updated_collection",
        "metadata": {"description": "An updated collection"},
        "num_documents": 5,
    }

    responses.add(
        responses.PATCH,
        f"{base_url}/v1/collections/test_collection/",
        json=expected_out,
        status=200,
    )

    collection = client.partial_update_collection(
        collection_name="test_collection",
        name="updated_collection",
        metadata={"description": "An updated collection"},
    )
    assert isinstance(collection, CollectionOut)
    assert collection.id == 1
    assert collection.name == "updated_collection"
    assert collection.metadata == {"description": "An updated collection"}
    assert collection.num_documents == 5


@responses.activate
def test_partial_update_collection_not_found_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_detail = {"detail": "Collection 'test_collection' not found."}

    responses.add(
        responses.PATCH,
        f"{base_url}/v1/collections/test_collection/",
        json=error_detail,
        status=404,
    )

    with pytest.raises(Exception) as exc_info:
        client.partial_update_collection(
            collection_name="test_collection",
            name="updated_collection",
            metadata={"description": "An updated collection"},
        )
    assert "Collection 'test_collection' not found." in str(exc_info.value)


@responses.activate
def test_partial_update_collection_missing_params_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    with pytest.raises(Exception) as exc_info:
        client.partial_update_collection(collection_name="test_collection")
    assert (
        "validation error for PatchCollectionIn\n  Value error, At least one field must be provided to update."
        in str(exc_info.value)
    )


@responses.activate
def test_partial_update_collection_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.PATCH,
        f"{base_url}/v1/collections/test_collection/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.partial_update_collection(
            collection_name="test_collection", name="updated_collection"
        )


@responses.activate
def test_delete_collection_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    responses.add(
        responses.DELETE, f"{base_url}/v1/collections/test_collection/", status=204
    )

    out = client.delete_collection(collection_name="test_collection")
    assert out is None


@responses.activate
def test_delete_collection_not_found_sync(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_detail = {"detail": "Collection 'test_collection' not found."}

    responses.add(
        responses.DELETE,
        f"{base_url}/v1/collections/test_collection/",
        json=error_detail,
        status=404,
    )

    with pytest.raises(Exception) as exc_info:
        client.delete_collection(collection_name="test_collection")
    assert "Collection 'test_collection' not found." in str(exc_info.value)


@responses.activate
def test_delete_collection_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.DELETE,
        f"{base_url}/v1/collections/test_collection/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.delete_collection(collection_name="test_collection")


@responses.activate
def test_add_webhook(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # mock the response for the add webhook request
    responses.add(
        responses.POST,
        f"{base_url}/v1/webhook/",
        json={
            "app_id": "test_app_id",
            "endpoint_id": "test_endpoint_id",
            "webhook_secret": "test_webhook_secret",
        },
        status=200,
    )

    webhook_url = "https://webhook.site/1234"
    response = client.add_webhook(webhook_url)
    assert isinstance(response, WebhookOut)


@responses.activate
def test_add_webhook_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # mock the response for the add webhook request,
    responses.add(
        responses.POST,
        f"{base_url}/v1/webhook/",
        json={"detail": "Error adding webhook: "},
        status=400,
    )

    webhook_url = "https://webhook.site/1234"

    with pytest.raises(ValueError):
        client.add_webhook(webhook_url)


@responses.activate
def test_add_webhook_unexpected_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # mock the response for the add webhook request,
    responses.add(
        responses.POST,
        f"{base_url}/v1/webhook/",
        json={"detail": "Error adding webhook: "},
        status=500,
    )

    webhook_url = "https://webhook.site/1234"

    with pytest.raises(HTTPError):
        client.add_webhook(webhook_url)


@responses.activate
def test_validate_webhook(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # Mock webhook verify
    with patch("colivara_py.client.Webhook") as MockWebhook:
        # Create a mock instance of SvixAsync
        mock_webhook = MagicMock()
        MockWebhook.return_value = mock_webhook

        # Set return values for the mocked methods
        mock_webhook.verify.return_value = True

        # call the validate_webhook method
        # These were all sent from the server
        headers = {
            "svix-id": "msg_p5jXN8AQM9LWM0D4loKWxJek",
            "svix-timestamp": "1614265330",
            "svix-signature": "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
        }
        payload = '{"test": 2432232314}'
        out = client.validate_webhook("test_webhook_secre", payload, headers)
        assert out


@responses.activate
def test_validate_webhook_failure(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    # Mock webhook verify
    with patch("colivara_py.client.Webhook") as MockWebhook:
        # Create a mock instance of SvixAsync
        mock_webhook = MagicMock()
        MockWebhook.return_value = mock_webhook

        # make the mocked method throw an exception
        mock_webhook.verify.side_effect = Exception("Error verifying webhook")

        # call the validate_webhook method
        # These were all sent from the server
        headers = {
            "svix-id": "msg_p5jXN8AQM9LWM0D4loKWxJek",
            "svix-timestamp": "1614265330",
            "svix-signature": "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
        }
        payload = '{"test": 2432232314}'
        out = client.validate_webhook("test_webhook_secre", payload, headers)
        assert not out


@responses.activate
def test_upsert_document_async_sync(api_key, tmp_path):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "detail": "Document is being processed in the background.",
    }

    responses.add(
        responses.POST,
        f"{base_url}/v1/documents/upsert-document/",
        json=expected_out,
        status=202,
    )

    # Test with base64 content
    response = client.upsert_document(
        name="test_document",
        metadata={"description": "A test document"},
        document_base64="dGVzdCBkb2N1bWVudCBjb250ZW50",
    )
    assert isinstance(response, GenericMessage)

    # Test with file path
    test_file = tmp_path / "test_document.txt"
    test_file.write_text("test document content")

    response = client.upsert_document(
        name="test_document_from_file",
        metadata={"description": "A test document from file"},
        document_path=str(test_file),
    )
    assert isinstance(response, GenericMessage)

    # Test with URL
    response = client.upsert_document(
        name="test_document_from_url",
        metadata={"description": "A test document from URL"},
        document_url="https://pdfobject.com/pdf/sample.pdf",
    )
    assert isinstance(response, GenericMessage)


@responses.activate
def test_upsert_document_sync(api_key, tmp_path):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "id": 1,
        "name": "test_document",
        "metadata": {"description": "A test document"},
        "collection_name": "default_collection",
        # aws s3 url
        "url": "https://colivara.s3.amazonaws.com/documents/test_document.pdf",
        "num_pages": 1,
    }

    responses.add(
        responses.POST,
        f"{base_url}/v1/documents/upsert-document/",
        json=expected_out,
        status=201,
    )

    # Test with base64 content
    document = client.upsert_document(
        name="test_document",
        metadata={"description": "A test document"},
        document_base64="dGVzdCBkb2N1bWVudCBjb250ZW50",
    )
    assert isinstance(document, DocumentOut)
    assert document.id == 1
    assert document.name == "test_document"
    assert document.metadata == {"description": "A test document"}
    assert document.collection_name == "default_collection"
    assert (
        document.url == "https://colivara.s3.amazonaws.com/documents/test_document.pdf"
    )
    assert document.num_pages == 1

    # Test with file path
    test_file = tmp_path / "test_document.txt"
    test_file.write_text("test document content")

    document = client.upsert_document(
        name="test_document_from_file",
        metadata={"description": "A test document from file"},
        document_path=str(test_file),
    )
    assert isinstance(document, DocumentOut)
    assert document.id == 1
    assert document.name == "test_document"
    assert document.metadata == {"description": "A test document"}
    assert document.collection_name == "default_collection"
    assert (
        document.url == "https://colivara.s3.amazonaws.com/documents/test_document.pdf"
    )
    assert document.num_pages == 1

    # Test with URL
    document = client.upsert_document(
        name="test_document_from_url",
        metadata={"description": "A test document from URL"},
        document_url="https://pdfobject.com/pdf/sample.pdf",
    )
    assert isinstance(document, DocumentOut)
    assert document.id == 1
    assert document.name == "test_document"
    assert document.metadata == {"description": "A test document"}
    assert document.collection_name == "default_collection"
    assert (
        document.url == "https://colivara.s3.amazonaws.com/documents/test_document.pdf"
    )
    assert document.num_pages == 1


@responses.activate
def test_upsert_document_sync_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    responses.add(
        responses.POST,
        f"{base_url}/v1/documents/upsert-document/",
        json={"detail": "Bad request error"},
        status=400,
    )

    with pytest.raises(ValueError, match="Bad request: Bad request error"):
        client.upsert_document(name="test_document", document_base64="invalid_base64")


@responses.activate
def test_upsert_document_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.POST,
        f"{base_url}/v1/documents/upsert-document/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.upsert_document(name="test_document", document_base64="invalid_base64")


@pytest.mark.parametrize(
    "input_data, expected_exception, expected_message",
    [
        (
            {"name": "test_document"},
            ValueError,
            "Either document_url, document_base64, or document_path must be provided.",
        ),
        (
            {
                "name": "test_document",
                "document_url": None,
                "document_base64": None,
                "document_path": None,
            },
            ValueError,
            "Either document_url, document_base64, or document_path must be provided.",
        ),
        (
            {
                "name": "test_document",
                "document_path": "/non/existent/path/file.txt",
            },
            FileNotFoundError,
            "The specified file does not exist: /non/existent/path/file.txt",
        ),
        (
            {
                "name": "test_document",
                "document_path": str(
                    Path(__file__).parent
                ),  # Use the directory of the test file
            },
            ValueError,
            "The specified path is not a file:",
        ),
        (
            {
                "name": "test_document",
                "document_path": "/root/restricted_file.txt",  # Assume this file exists but is not readable
            },
            ValueError,
            "Error reading file:",
        ),
    ],
)
def test_upsert_document_sync_invalid_input(
    api_key, input_data, expected_exception, expected_message, monkeypatch
):
    os.environ["COLIVARA_API_KEY"] = api_key
    client = ColiVara(base_url="https://api.test.com")

    # Mock os.access to simulate permission error
    def mock_access(path, mode):
        return str(path) != "/root/restricted_file.txt"

    monkeypatch.setattr(os, "access", mock_access)

    # Mock Path.is_file to simulate directory instead of file
    def mock_is_file(self):
        return str(self) != str(Path(__file__).parent)

    monkeypatch.setattr(Path, "is_file", mock_is_file)

    with pytest.raises(expected_exception, match=expected_message):
        client.upsert_document(**input_data)


@responses.activate
def test_get_document(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "id": 1,
        "name": "test_document",
        "metadata": {"description": "A test document"},
        "collection_name": "default_collection",
        "url": "https://colivara.s3.amazonaws.com/documents/test_document.pdf",
        "num_pages": 1,
    }

    responses.add(
        responses.GET,
        f"{base_url}/v1/documents/test_document/",
        json=expected_out,
        status=200,
    )

    document = client.get_document("test_document")
    assert isinstance(document, DocumentOut)
    assert document.id == 1
    assert document.name == "test_document"
    assert document.metadata == {"description": "A test document"}
    assert document.collection_name == "default_collection"
    assert (
        document.url == "https://colivara.s3.amazonaws.com/documents/test_document.pdf"
    )
    assert document.num_pages == 1


@responses.activate
def test_get_document_not_found(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    responses.add(
        responses.GET,
        f"{base_url}/v1/documents/non_existent_document/",
        json={"detail": "Document not found"},
        status=404,
    )

    with pytest.raises(ValueError, match="Document not found: Document not found"):
        client.get_document("non_existent_document")


@responses.activate
def test_get_document_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.GET,
        f"{base_url}/v1/documents/test_document/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.get_document("test_document")


@responses.activate
def test_partial_update_document(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "id": 1,
        "name": "updated_document",
        "metadata": {"description": "An updated test document"},
        "collection_name": "default_collection",
        "url": "https://colivara.s3.amazonaws.com/documents/test_document.pdf",
        "num_pages": 1,
    }

    responses.add(
        responses.PATCH,
        f"{base_url}/v1/documents/test_document/",
        json=expected_out,
        status=200,
    )

    document = client.partial_update_document(
        "test_document",
        name="updated_document",
        metadata={"description": "An updated test document"},
    )
    assert isinstance(document, DocumentOut)
    assert document.id == 1
    assert document.name == "updated_document"
    assert document.metadata == {"description": "An updated test document"}


@responses.activate
def test_partial_update_document_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    responses.add(
        responses.PATCH,
        f"{base_url}/v1/documents/non_existent_document/",
        json={"detail": "Document not found"},
        status=404,
    )

    with pytest.raises(ValueError, match="Update failed: Document not found"):
        client.partial_update_document("non_existent_document", name="updated_document")


@responses.activate
def test_partial_update_document_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.PATCH,
        f"{base_url}/v1/documents/test_document/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.partial_update_document("test_document", name="updated_document")


@responses.activate
def test_list_documents(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = [
        {
            "id": 1,
            "name": "document1",
            "metadata": {"description": "First document"},
            "collection_name": "default_collection",
            "url": "https://colivara.s3.amazonaws.com/documents/document1.pdf",
            "num_pages": 1,
        },
        {
            "id": 2,
            "name": "document2",
            "metadata": {"description": "Second document"},
            "collection_name": "default_collection",
            "url": "https://colivara.s3.amazonaws.com/documents/document2.pdf",
            "num_pages": 2,
        },
    ]

    responses.add(
        responses.GET, f"{base_url}/v1/documents/", json=expected_out, status=200
    )

    documents = client.list_documents()
    assert isinstance(documents, list)
    assert len(documents) == 2
    assert all(isinstance(doc, DocumentOut) for doc in documents)
    assert documents[0].name == "document1"
    assert documents[1].name == "document2"


@responses.activate
def test_list_documents_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.GET,
        f"{base_url}/v1/documents/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.list_documents()


@responses.activate
def test_delete_document(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    responses.add(
        responses.DELETE,
        f"{base_url}/v1/documents/delete-document/test_document/",
        status=204,
    )

    client.delete_document("test_document")
    # If no exception is raised, the test passes


@responses.activate
def test_delete_document_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    responses.add(
        responses.DELETE,
        f"{base_url}/v1/documents/delete-document/non_existent_document/",
        json={"detail": "Document not found"},
        status=404,
    )

    with pytest.raises(ValueError, match="Deletion failed: Document not found"):
        client.delete_document("non_existent_document")


@responses.activate
def test_delete_document_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.DELETE,
        f"{base_url}/v1/documents/delete-document/test_document/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.delete_document("test_document")


@responses.activate
def test_search_simple(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "query": "what is 1+1?",
        "results": [
            {
                "collection_name": "default",
                "collection_id": 1,
                "document_name": "math_doc",
                "document_id": 1,
                "page_number": 1,
                "raw_score": 0.9,
                "normalized_score": 0.95,
                "img_base64": "base64_encoded_image",
            }
        ],
    }

    responses.add(
        responses.POST, f"{client.base_url}/v1/search/", json=expected_out, status=200
    )

    result = client.search("what is 1+1?")
    assert isinstance(result, QueryOut)
    assert result.query == "what is 1+1?"
    assert len(result.results) == 1
    assert isinstance(result.results[0], PageOutQuery)
    assert result.results[0].document_name == "math_doc"


@responses.activate
def test_search_with_collection(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "query": "what is 1+1?",
        "results": [
            {
                "collection_name": "my_collection",
                "collection_id": 2,
                "document_name": "math_doc",
                "document_id": 1,
                "page_number": 1,
                "raw_score": 0.9,
                "normalized_score": 0.95,
                "img_base64": "base64_encoded_image",
            }
        ],
    }

    responses.add(
        responses.POST, f"{client.base_url}/v1/search/", json=expected_out, status=200
    )

    result = client.search("what is 1+1?", collection_name="my_collection")
    assert isinstance(result, QueryOut)
    assert result.results[0].collection_name == "my_collection"


@responses.activate
def test_search_with_filter(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "query": "what is 1+1?",
        "results": [
            {
                "collection_name": "default",
                "collection_id": 1,
                "document_name": "math_doc",
                "document_id": 1,
                "page_number": 1,
                "raw_score": 0.9,
                "normalized_score": 0.95,
                "img_base64": "base64_encoded_image",
                "document_metadata": {"category": "AI"},
            }
        ],
    }

    responses.add(
        responses.POST, f"{client.base_url}/v1/search/", json=expected_out, status=200
    )

    query_filter = {
        "on": "document",
        "key": "category",
        "value": "AI",
        "lookup": "contains",
    }
    result = client.search("what is 1+1?", query_filter=query_filter)
    assert isinstance(result, QueryOut)
    assert result.results[0].document_metadata["category"] == "AI"


@responses.activate
def test_filter_documents(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = [
        {
            "id": 1,
            "name": "Test Document Fixture",
            "metadata": {"important": True},
            "url": "https://www.example.com",
            "num_pages": 1,
            "collection_name": "Test Collection Fixture",
        }
    ]

    responses.add(
        responses.POST, f"{client.base_url}/v1/filter/", json=expected_out, status=200
    )

    query_filter = {
        "on": "document",
        "key": "important",
        "value": True,
    }
    result = client.filter(query_filter=query_filter)
    assert isinstance(result, list)
    assert len(result) == 1


@responses.activate
def test_filter_documents_expand(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = [
        {
            "id": 1,
            "name": "Test Document Fixture",
            "metadata": {"important": True},
            "url": "https://www.example.com",
            "num_pages": 1,
            "collection_name": "Test Collection Fixture",
            "pages": [
                {
                    "document_name": "Test Document Fixture",
                    "img_base64": "base64_string",
                    "page_number": 1,
                }
            ],
        }
    ]

    responses.add(
        responses.POST,
        f"{client.base_url}/v1/filter/?expand=pages",
        json=expected_out,
        status=200,
    )

    query_filter = {
        "on": "document",
        "key": "important",
        "value": True,
    }
    result = client.filter(query_filter=query_filter, expand="pages")
    assert isinstance(result, list)
    assert len(result) == 1


@responses.activate
def test_filter_collections(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = [
        {
            "id": 1,
            "name": "test_collection",
            "metadata": {"description": "A test collection"},
            "num_documents": 2,
        },
        {
            "id": 2,
            "name": "another_test_collection",
            "metadata": {"description": "Another test collection"},
            "num_documents": 3,
        },
    ]

    responses.add(
        responses.POST, f"{client.base_url}/v1/filter/", json=expected_out, status=200
    )

    query_filter = {
        "on": "collection",
        "key": "important",
        "value": True,
    }
    result = client.filter(query_filter=query_filter, expand="pages")
    assert isinstance(result, list)
    assert len(result) == 2


@responses.activate
def test_search_service_unavailable(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_response = {"detail": "Service is temporarily unavailable"}

    responses.add(
        responses.POST, f"{client.base_url}/v1/search/", json=error_response, status=503
    )

    with pytest.raises(ValueError) as exc_info:
        client.search("what is 1+1?")

    assert "Service unavailable" in str(exc_info.value)


@responses.activate
def test_filter_service_unavailable(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    error_response = {"detail": "Service is temporarily unavailable"}

    responses.add(
        responses.POST, f"{client.base_url}/v1/filter/", json=error_response, status=503
    )

    with pytest.raises(ValueError) as exc_info:
        client.filter(
            query_filter={
                "on": "document",
                "key": "category",
                "value": "AI",
                "lookup": "contains",
            }
        )

    assert "Service unavailable" in str(exc_info.value)


@responses.activate
def test_search_invalid_filter(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    with pytest.raises(ValueError) as exc_info:
        client.search("what is 1+1?", query_filter={"invalid": "filter"})

    assert "Invalid query_filter" in str(exc_info.value)


@responses.activate
def test_filter_invalid_filter(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    with pytest.raises(ValueError) as exc_info:
        client.filter(query_filter={"invalid": "filter"})

    assert "Invalid query_filter" in str(exc_info.value)


@responses.activate
def test_search_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.POST,
        f"{client.base_url}/v1/search/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.search("what is 1+1?")


@responses.activate
def test_filter_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.POST,
        f"{client.base_url}/v1/filter/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.filter(
            query_filter={
                "on": "document",
                "key": "category",
                "value": "AI",
                "lookup": "contains",
            }
        )


@pytest.fixture
def test_file_path(tmp_path):
    file_content = b"Test file content"
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "wb") as f:
        f.write(file_content)
    return str(file_path)


@responses.activate
def test_file_to_imgbase64(api_key, test_file_path):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = [
        {"img_base64": base64.b64encode(b"Test image 1").decode(), "page_number": 1},
        {"img_base64": base64.b64encode(b"Test image 2").decode(), "page_number": 2},
    ]

    responses.add(
        responses.POST,
        f"{base_url}/v1/helpers/file-to-imgbase64/",
        json=expected_out,
        status=200,
    )

    result = client.file_to_imgbase64(test_file_path)

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, FileOut) for item in result)
    assert result[0].img_base64 == expected_out[0]["img_base64"]
    assert result[0].page_number == 1
    assert result[1].img_base64 == expected_out[1]["img_base64"]
    assert result[1].page_number == 2


@responses.activate
def test_file_to_imgbase64_http_error(api_key, test_file_path):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.POST,
        f"{base_url}/v1/helpers/file-to-imgbase64/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.file_to_imgbase64(test_file_path)


@responses.activate
def test_file_to_base64(api_key, test_file_path):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = base64.b64encode(b"Test file content").decode()

    responses.add(
        responses.POST,
        f"{base_url}/v1/helpers/file-to-base64/",
        body=expected_out,
        status=200,
    )

    result = client.file_to_base64(test_file_path)

    assert isinstance(result, str)
    assert result == expected_out


@responses.activate
def test_create_embedding(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)

    expected_out = {
        "data": [
            {
                "embedding": [[0.10986328125, -0.08251953125, 0.005767822265625]],
                "index": 0,
                "object": "embedding",
            }
        ],
        "model": "vidore/colQwen-v1.2",
        "usage": {"prompt_tokens": 24, "total_tokens": 24},
    }

    responses.add(
        responses.POST, f"{base_url}/v1/embeddings/", json=expected_out, status=200
    )

    # Test with a single string input
    embedding_result = client.create_embedding("what is 1+1?", task="query")

    assert isinstance(embedding_result, EmbeddingsOut)
    assert len(embedding_result.data) == 1
    assert embedding_result.data[0]["embedding"] == [
        [0.10986328125, -0.08251953125, 0.005767822265625]
    ]
    assert embedding_result.data[0]["index"] == 0
    assert embedding_result.data[0]["object"] == "embedding"
    assert embedding_result.model == "vidore/colQwen-v1.2"
    assert embedding_result.usage == {"prompt_tokens": 24, "total_tokens": 24}

    # Test with a list of strings input
    responses.add(
        responses.POST, f"{base_url}/v1/embeddings/", json=expected_out, status=200
    )

    embedding_result = client.create_embedding(
        ["base64string_1", "base64string_1"], task="image"
    )

    assert isinstance(embedding_result, EmbeddingsOut)
    assert (
        len(embedding_result.data) == 1
    )  # In this case, we're using the same mock response
    assert embedding_result.data[0]["embedding"] == [
        [0.10986328125, -0.08251953125, 0.005767822265625]
    ]
    assert embedding_result.model == "vidore/colQwen-v1.2"

    with tempfile.NamedTemporaryFile(
        suffix=".png", delete=False
    ) as f1, tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f2:
        # Write some dummy data if needed
        f1.write(b"test data")
        f2.write(b"test data")

        responses.add(
            responses.POST, f"{base_url}/v1/embeddings/", json=expected_out, status=200
        )
        embedding_result = client.create_embedding([f1.name, f2.name], task="image")

        assert isinstance(embedding_result, EmbeddingsOut)
        assert (
            len(embedding_result.data) == 1
        )  # In this case, we're using the same mock response
        assert embedding_result.data[0]["embedding"] == [
            [0.10986328125, -0.08251953125, 0.005767822265625]
        ]
        assert embedding_result.model == "vidore/colQwen-v1.2"

        # Clean up
        os.unlink(f1.name)
        os.unlink(f2.name)

    # Test error handling
    responses.add(
        responses.POST,
        f"{base_url}/v1/embeddings/",
        json={"detail": "Service is temporarily unavailable"},
        status=503,
    )

    with pytest.raises(Exception) as exc_info:
        client.create_embedding("error test", task="query")

    assert (
        str(exc_info.value) == "Service Unavailable: Service is temporarily unavailable"
    )

    # Test invalid task
    with pytest.raises(ValueError) as exc_info:
        client.create_embedding("invalid task test", task="invalid")

    assert str(exc_info.value) == "Invalid task: invalid. Must be 'query' or 'image'."

    # test non srting task
    with pytest.raises(ValueError) as exc_info:
        client.create_embedding("invalid task test", task=123)

    assert str(exc_info.value) == "Task must be a string or TaskEnum."

    # test with non string input
    with pytest.raises(ValueError) as exc_info:
        client.create_embedding(123, task="query")


@responses.activate
def test_create_embedding_http_error(api_key):
    os.environ["COLIVARA_API_KEY"] = api_key
    base_url = "https://api.test.com"
    client = ColiVara(base_url=base_url)
    responses.add(
        responses.POST,
        f"{base_url}/v1/embeddings/",
        json={"error": "Internal Server Error"},
        status=500,
    )
    with pytest.raises(HTTPError):
        client.create_embedding("what is 1+1?", task="query")


""" MISC TESTS """


def test_async_colivara_not_implemented():
    with pytest.raises(
        NotImplementedError, match="AsyncColiVara is not implemented yet."
    ):
        AsyncColiVara()


def test_patch_collection_in_invalid_name():
    with pytest.raises(ValueError, match="Collection name 'all' is not allowed."):
        PatchCollectionIn(name="all", metadata={"key": "value"})


def test_document_in_invalid():
    with pytest.raises(ValueError, match="Either 'url' or 'base64' must be provided."):
        DocumentIn(name="test_document", metadata={"description": "A test document"})

    with pytest.raises(
        ValueError, match="Only one of 'url' or 'base64' should be provided."
    ):
        DocumentIn(
            name="test_document",
            metadata={"description": "A test document"},
            url="https://pdfobject.com/pdf/sample.pdf",
            base64="base64_string",
        )


def test_document_patch_in_invalid():
    with pytest.raises(
        ValueError, match="At least one field must be provided to update."
    ):
        DocumentInPatch(coollection_name="test_collection")

    with pytest.raises(
        ValueError, match="Only one of 'url' or 'base64' should be provided."
    ):
        DocumentInPatch(
            name="test_document",
            url="https://pdfobject.com/pdf/sample.pdf",
            base64="base64_string",
        )


@pytest.mark.parametrize(
    "on, key, value, lookup, should_raise",
    [
        # Test cases for "contains" and "contained_by"
        ("document", "key1", "value1", "contains", False),
        ("document", "key1", None, "contains", True),
        ("document", ["key1"], "value1", "contains", True),
        ("document", "key1", "value1", "contained_by", False),
        ("document", "key1", None, "contained_by", True),
        ("document", ["key1"], "value1", "contained_by", True),
        # Test cases for "key_lookup"
        ("document", "key1", "value1", "key_lookup", False),
        ("document", "key1", None, "key_lookup", True),
        ("document", ["key1"], "value1", "key_lookup", True),
        # Test cases for "has_key"
        ("document", "key1", None, "has_key", False),
        ("document", "key1", "value1", "has_key", True),
        ("document", ["key1"], None, "has_key", True),
        # Test cases for "has_keys"
        ("document", ["key1", "key2"], None, "has_keys", False),
        ("document", "key1", None, "has_keys", True),
        ("document", ["key1", "key2"], "value1", "has_keys", True),
        # Test cases for "has_any_keys"
        ("document", ["key1", "key2"], None, "has_any_keys", False),
        ("document", ["key1", "key2"], "value1", "has_any_keys", True),
    ],
)
def test_query_filter_validation(on, key, value, lookup, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            QueryFilter(on=on, key=key, value=value, lookup=lookup)
    else:
        filter_instance = QueryFilter(on=on, key=key, value=value, lookup=lookup)
        assert filter_instance.key == key if isinstance(key, list) else [key]
        assert filter_instance.value == value
        assert filter_instance.lookup == lookup
