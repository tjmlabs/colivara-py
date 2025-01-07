import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from colivara_py import ColiVara
from colivara_py.exceptions import ApiException
from colivara_py.models import TaskEnum
from colivara_py.models import (
    CollectionIn,
    DocumentIn,
    QueryIn,
    EmbeddingsIn,
    DocumentInPatch,
)
from pathlib import Path
import re
import base64


@pytest.fixture
def client():
    """Fixture for initialized client"""
    with patch.dict(os.environ, {"COLIVARA_API_KEY": "test-key"}):
        return ColiVara()


@pytest.fixture
def api_key():
    """Fixture for API key"""
    return "test-api-key"


@pytest.fixture
def mock_api_response():
    """Fixture for mocked API response"""
    return MagicMock()


# Initialization Tests
def test_init_with_explicit_api_key():
    """Test initialization with explicit API key"""
    client = ColiVara(api_key="test-key")
    assert client.api_key == "test-key"
    assert client.config.host == "https://api.colivara.com"


def test_init_with_env_api_key():
    """Test initialization with environment variable API key"""
    with patch.dict(os.environ, {"COLIVARA_API_KEY": "env-key"}):
        client = ColiVara()
        assert client.api_key == "env-key"


def test_init_without_api_key():
    """Test initialization without API key raises error"""
    with patch.dict(os.environ, clear=True):
        with pytest.raises(ValueError, match="API key must be provided"):
            ColiVara()


def test_init_with_custom_base_url():
    """Test initialization with custom base URL"""
    client = ColiVara(api_key="test-key", base_url="https://custom.api.com")
    assert client.config.host == "https://custom.api.com"


# Collection Tests
def test_get_collection(client, mock_api_response):
    """Test get collection endpoint"""
    client.collections_api.api_views_get_collection = MagicMock(
        return_value=mock_api_response
    )
    result = client.get_collection("test-collection")
    assert result == mock_api_response
    client.collections_api.api_views_get_collection.assert_called_once_with(
        "test-collection"
    )


def test_get_collection_error(client):
    """Test get collection error handling"""
    error = ApiException(status=404, reason="Not Found")
    client.collections_api.api_views_get_collection = MagicMock(side_effect=error)
    with pytest.raises(RuntimeError, match="API Error: 404 - Not Found"):
        client.get_collection("test-collection")


def test_create_collection(client, mock_api_response):
    """Test create collection endpoint"""
    client.collections_api.api_views_create_collection = MagicMock(
        return_value=mock_api_response
    )
    result = client.create_collection("test-name", {"key": "value"})
    assert result == mock_api_response
    client.collections_api.api_views_create_collection.assert_called_once_with(
        CollectionIn(name="test-name", metadata={"key": "value"})
    )


def test_create_collection_no_metadata(client, mock_api_response):
    """Test create collection without metadata"""
    client.collections_api.api_views_create_collection = MagicMock(
        return_value=mock_api_response
    )
    result = client.create_collection("test-name")
    assert result == mock_api_response
    client.collections_api.api_views_create_collection.assert_called_once_with(
        CollectionIn(name="test-name", metadata={})
    )


def test_partial_update_collection(client, mock_api_response):
    """Test partial update collection endpoint"""
    client.collections_api.api_views_partial_update_collection = MagicMock(
        return_value=mock_api_response
    )
    result = client.partial_update_collection(
        collection_name="test-collection", name="new-name", metadata={"key": "value"}
    )
    assert result == mock_api_response
    client.collections_api.api_views_partial_update_collection.assert_called_once()


def test_list_collections(client, mock_api_response):
    """Test list collections endpoint"""
    client.collections_api.api_views_list_collections = MagicMock(
        return_value=mock_api_response
    )
    result = client.list_collections()
    assert result == mock_api_response
    client.collections_api.api_views_list_collections.assert_called_once()


def test_delete_collection(client):
    """Test delete collection endpoint"""
    client.collections_api.api_views_delete_collection = MagicMock()
    client.delete_collection("test-collection")
    client.collections_api.api_views_delete_collection.assert_called_once_with(
        "test-collection"
    )


# Document Tests
def test_upsert_document(client, mock_api_response):
    """Test upsert document endpoint"""
    client.documents_api.api_views_upsert_document = MagicMock(
        return_value=mock_api_response
    )
    result = client.upsert_document(
        name="test-doc",
        collection_name="test-collection",
        document_url="http://test.url",
        metadata={"key": "value"},
    )
    assert result == mock_api_response
    client.documents_api.api_views_upsert_document.assert_called_once_with(
        DocumentIn(
            name="test-doc",
            collection_name="test-collection",
            url="http://test.url",
            metadata={"key": "value"},
            wait=False,
            use_proxy=False,
        )
    )


def test_upsert_document_file_handling():
    client = ColiVara(api_key="test-key")

    # Test not a file error
    with patch("pathlib.Path.is_file", return_value=False):
        with patch("pathlib.Path.resolve", return_value=Path("not_a_file")):
            with pytest.raises(
                ValueError, match="The specified path is not a file: not_a_file"
            ):
                client.upsert_document("test", document_path="not_a_file")

    # Test permission error
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("pathlib.Path.resolve", return_value=Path("test.txt")):
            with patch("os.access", return_value=False):
                with pytest.raises(
                    ValueError,
                    match="Error reading file: No read permission for file: test.txt",
                ):
                    client.upsert_document("test", document_path="test.txt")

    # Test file read error
    with patch("pathlib.Path.is_file", return_value=True):
        with patch("pathlib.Path.resolve", return_value=Path("test.txt")):
            with patch("os.access", return_value=True):
                with patch("builtins.open", mock_open()) as mock_file:
                    mock_file.side_effect = Exception("Read error")
                    with pytest.raises(
                        ValueError, match="Error reading file: Read error"
                    ):
                        client.upsert_document("test", document_path="test.txt")


def test_upsert_document_validation():
    client = ColiVara(api_key="test-key")

    # Test missing document source error
    with pytest.raises(
        ValueError,
        match="Either document_url, document_base64, or document_path must be provided",
    ):
        client.upsert_document("test", "collection")


def test_get_document(client, mock_api_response):
    """Test get document endpoint"""
    client.documents_api.api_views_get_document = MagicMock(
        return_value=mock_api_response
    )
    result = client.get_document("test-doc", "test-collection")
    assert result == mock_api_response
    client.documents_api.api_views_get_document.assert_called_once_with(
        "test-doc", "test-collection", None
    )


def test_list_documents(client, mock_api_response):
    """Test list documents endpoint"""
    client.documents_api.api_views_list_documents = MagicMock(
        return_value=mock_api_response
    )
    result = client.list_documents("test-collection")
    assert result == mock_api_response
    client.documents_api.api_views_list_documents.assert_called_once_with(
        collection_name="test-collection", expand=None
    )


def test_delete_document(client):
    """Test delete document endpoint"""
    client.documents_api.api_views_delete_document = MagicMock()
    client.delete_document("test-doc", "test-collection")
    client.documents_api.api_views_delete_document.assert_called_once_with(
        "test-doc", "test-collection"
    )


# Filter Tests
def test_filter_with_complete_params(client, mock_api_response):
    """Test filter endpoint with all parameters"""
    client.filter_api.api_views_filter = MagicMock(return_value=mock_api_response)
    query_filter = {
        "key": "test-key",
        "value": "test-value",
        "lookup": "contains",
        "on": "document",
    }
    result = client.filter(query_filter, expand="test-expand")
    assert result == mock_api_response.actual_instance


def test_filter_missing_required_key(client):
    """Test filter with missing required key"""
    with pytest.raises(ValueError, match="Missing required key"):
        client.filter({"value": "test"})


def test_filter_unexpected_error(client):
    """Test filter unexpected error handling"""
    client.filter_api.api_views_filter = MagicMock(side_effect=Exception("Unexpected"))
    with pytest.raises(Exception, match="An unexpected error occurred"):
        client.filter({"key": "test", "value": "test", "lookup": "contains"})


# File Operations Tests
def test_file_to_base64():
    """Test file to base64 conversion"""
    client = ColiVara(api_key="test-key")
    mock_content = b"test content"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = client.file_to_base64("test.txt")
        assert isinstance(result, str)


def test_file_to_imgbase64(client, mock_api_response):
    """Test file to image base64 conversion"""
    client.helpers_api.api_views_file_to_imgbase64 = MagicMock(
        return_value=mock_api_response
    )
    with patch("builtins.open", mock_open(read_data=b"test")):
        result = client.file_to_imgbase64("test.jpg")
        assert result == mock_api_response


# Search Tests
def test_search_with_filter(client, mock_api_response):
    """Test search endpoint with filter"""
    client.search_api.api_views_search = MagicMock(return_value=mock_api_response)
    result = client.search(
        "test query",
        "test-collection",
        top_k=5,
        query_filter={
            "key": "test",
            "value": "test",
            "lookup": "contains",
            "on": "document",
        },
    )
    assert result == mock_api_response


def test_search_with_minimum_params(client, mock_api_response):
    """Test search with minimum required parameters"""
    client.search_api.api_views_search = MagicMock(return_value=mock_api_response)
    result = client.search("test query", "test-collection")
    assert result == mock_api_response
    client.search_api.api_views_search.assert_called_once_with(
        QueryIn(
            query="test query",
            collection_name="test-collection",
            top_k=3,
            query_filter=None,
        )
    )


# Embedding Tests
def test_create_embedding_with_list_input(client, mock_api_response):
    """Test create embedding with list input"""
    client.embeddings_api.api_views_embeddings = MagicMock(
        return_value=mock_api_response
    )
    input_data = ["text1", "text2"]
    result = client.create_embedding(input_data, TaskEnum.IMAGE)
    assert result == mock_api_response
    client.embeddings_api.api_views_embeddings.assert_called_once_with(
        EmbeddingsIn(input_data=input_data, task=TaskEnum.IMAGE)
    )


# Webhook Tests
def test_add_webhook(client, mock_api_response):
    """Test add webhook endpoint"""
    client.webhook_api.api_views_add_webhook = MagicMock(return_value=mock_api_response)
    result = client.add_webhook("http://test.webhook")
    assert result == mock_api_response


# Health Check Tests
def test_check_health(client):
    """Test health check endpoint"""
    client.health_api.api_views_health = MagicMock()
    client.check_health()
    client.health_api.api_views_health.assert_called_once()


# Error Handling Tests
@pytest.mark.parametrize(
    "error_code,error_message,expected_message",
    [
        (409, "Conflict", "Conflict: The request could not be completed"),
        (
            503,
            "Service Unavailable",
            "Service Unavailable: The server is not ready to handle",
        ),
        (401, "Unauthorized", "Unauthorized: Access is denied due to"),
        (403, "Forbidden", "Forbidden: You do not have permission"),
        (
            429,
            "Too Many Requests",
            "Too Many Requests: You have sent too many requests",
        ),
        (
            500,
            "Server Error",
            "Internal Server Error: The server encountered an unexpected condition",
        ),
    ],
)
def test_error_handling(client, error_code, error_message, expected_message):
    """Test all error handling scenarios in one test"""
    error = ApiException(status=error_code, reason=error_message)
    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert expected_message in str(exc_info.value)


def test_handle_error_default_case():
    """Test error handling for unexpected status code"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=599, reason="Unknown Error")
    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert "Unexpected Error: 599" in str(exc_info.value)


def test_handle_error_without_body_headers():
    """Test error handling without body and headers"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=404, reason="Not Found")
    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert "API Error: 404 - Not Found" in str(exc_info.value)


def test_handle_error_minimal():
    """Test error handling with minimal information"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=400, reason="Bad Request")
    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert "API Error: 400 - Bad Request" in str(exc_info.value)


def test_handle_error_with_body_only():
    """Test error handling with body only"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=500, reason="Server Error")
    error.body = "Error Details"

    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert "API Error: 500 - Server Error" in str(exc_info.value)
    assert "Error Details" in str(exc_info.value)


def test_handle_error_with_falsy_status():
    """Test error handling when status attribute is falsy"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=404, reason="Not Found")
    # Set status to 0 to test falsy condition
    error.status = 0
    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert "API Error: 0 - Not Found" in str(exc_info.value)
    # Verify it doesn't include any specific error message since status is falsy
    assert "\n" not in str(exc_info.value)


def test_handle_error_with_bytes_body():
    """Test error handling with bytes body"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=500, reason="Server Error")
    error.body = b"Error Details in Bytes"

    with pytest.raises(RuntimeError) as exc_info:
        client._handle_error(error)
    assert "API Error: 500 - Server Error" in str(exc_info.value)
    assert "Error Details in Bytes" in str(exc_info.value)


def test_partial_update_document(client, mock_api_response):
    """Test partial update document endpoint"""
    client.documents_api.api_views_partial_update_document = MagicMock(
        return_value=mock_api_response
    )
    metadata = {"key": "updated_value"}
    result = client.partial_update_document(
        document_name="test-doc", collection_name="test-collection", metadata=metadata
    )
    assert result == mock_api_response
    client.documents_api.api_views_partial_update_document.assert_called_once_with(
        "test-doc",
        DocumentInPatch(
            collection_name="test-collection",
            metadata=metadata,
            name=None,
            url=None,
            base64=None,
            use_proxy=False,
        ),
    )


def test_partial_update_document_error(client):
    """Test partial update document error handling"""
    error = ApiException(status=404, reason="Document not found")
    client.documents_api.api_views_partial_update_document = MagicMock(
        side_effect=error
    )
    with pytest.raises(RuntimeError, match="API Error: 404 - Document not found"):
        client.partial_update_document("test-doc", "test-collection", {"key": "value"})


def test_upsert_document_with_path_valid_file(client, mock_api_response):
    """Test upsert document with a valid file path"""
    client.documents_api.api_views_upsert_document = MagicMock(
        return_value=mock_api_response
    )

    mock_file_content = b"test content"
    mock_base64_content = base64.b64encode(mock_file_content).decode("utf-8")

    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("pathlib.Path.resolve", return_value=Path("test.txt")),
        patch("os.access", return_value=True),
        patch("builtins.open", mock_open(read_data=mock_file_content)),
    ):
        result = client.upsert_document(
            name="test-doc", document_path="test.txt", collection_name="test-collection"
        )

        assert result == mock_api_response
        expected_body = DocumentIn(
            name="test-doc",
            metadata={},
            collection_name="test-collection",
            base64=mock_base64_content,
            wait=False,
            use_proxy=False,
        )
        client.documents_api.api_views_upsert_document.assert_called_once_with(
            expected_body
        )


def test_upsert_document_with_wait_and_proxy(client, mock_api_response):
    """Test upsert document with wait and use_proxy flags"""
    client.documents_api.api_views_upsert_document = MagicMock(
        return_value=mock_api_response
    )

    result = client.upsert_document(
        name="test-doc", document_url="http://test.url", wait=True, use_proxy=True
    )

    assert result == mock_api_response
    expected_body = DocumentIn(
        name="test-doc",
        metadata={},
        collection_name="default_collection",
        url="http://test.url",
        wait=True,
        use_proxy=True,
    )
    client.documents_api.api_views_upsert_document.assert_called_once_with(
        expected_body
    )


def test_upsert_document_path_and_url(client, mock_api_response):
    """Test upsert document with both path and URL provided"""
    client.documents_api.api_views_upsert_document = MagicMock(
        return_value=mock_api_response
    )

    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("pathlib.Path.resolve", return_value=Path("test.txt")),
        patch("os.access", return_value=True),
        patch("builtins.open", mock_open(read_data=b"test content")),
    ):
        result = client.upsert_document(
            name="test-doc",
            document_path="test.txt",
            document_url="http://test.url",
        )

        assert result == mock_api_response
        # Verify that both base64 and url are included in the request
        client.documents_api.api_views_upsert_document.assert_called_once()
        call_args = client.documents_api.api_views_upsert_document.call_args[0][0]
        assert (
            call_args.var_base64 == "dGVzdCBjb250ZW50"
        )  # base64 encoded "test content"
        assert call_args.url == "http://test.url"


def test_upsert_document_with_no_read_permission_error(client):
    """Test upsert document when file exists but has no read permission"""
    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("pathlib.Path.resolve", return_value=Path("test.txt")),
        patch("os.access", return_value=False),
    ):
        with pytest.raises(
            ValueError,
            match=r"Error reading file: No read permission for file: test\.txt",
        ):
            client.upsert_document(name="test-doc", document_path="test.txt")


def test_upsert_document_with_read_error(client):
    """Test upsert document when file read operation fails"""
    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("pathlib.Path.resolve", return_value=Path("test.txt")),
        patch("os.access", return_value=True),
        patch("builtins.open", side_effect=Exception("Read error")),
    ):
        with pytest.raises(ValueError, match="Error reading file: Read error"):
            client.upsert_document(name="test-doc", document_path="test.txt")


def test_upsert_document_file_not_found(client):
    """Test upsert document when file is not found"""
    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("os.access", return_value=True),
        patch("builtins.open", side_effect=FileNotFoundError("File not found")),
        pytest.raises(
            FileNotFoundError, match=r"The specified file does not exist: .*"
        ),
    ):
        client.upsert_document(name="test-doc", document_path="test.txt")


def test_file_to_imgbase64_error(client):
    """Test file to image base64 error handling"""
    error = ApiException(status=400, reason="Invalid file format")
    client.helpers_api.api_views_file_to_imgbase64 = MagicMock(side_effect=error)
    with patch("builtins.open", mock_open(read_data=b"test")):
        with pytest.raises(RuntimeError, match="API Error: 400 - Invalid file format"):
            client.file_to_imgbase64("test.jpg")


def test_check_health_error(client):
    """Test health check error handling"""
    error = ApiException(status=500, reason="Service unavailable")
    client.health_api.api_views_health = MagicMock(side_effect=error)
    with pytest.raises(RuntimeError, match="API Error: 500 - Service unavailable"):
        client.check_health()


def test_search_with_invalid_filter(client):
    """Test search with invalid filter"""
    invalid_filter = {
        "key": "test",
        "value": "test",
        "lookup": "invalid",
        "on": "invalid",
    }
    with pytest.raises(Exception) as exc_info:
        client.search("test query", "test-collection", query_filter=invalid_filter)
    assert "validation errors for QueryFilter" in str(exc_info.value)


def test_create_embedding_error(client):
    """Test create embedding error handling"""
    error = ApiException(status=400, reason="Invalid input data")
    client.embeddings_api.api_views_embeddings = MagicMock(side_effect=error)
    with pytest.raises(RuntimeError, match="API Error: 400 - Invalid input data"):
        client.create_embedding("test input", TaskEnum.QUERY)


def test_create_embedding_task_validation():
    client = ColiVara(api_key="test-key")

    # Test invalid task error
    with pytest.raises(
        ValueError, match=r"Invalid task: invalid_task\. Must be 'query' or 'image'"
    ):
        client.create_embedding("test", task="invalid_task")

    # Test file handling for image task
    with patch("pathlib.Path.is_file", return_value=True):
        error = ApiException(status=400, reason="Convert error")
        with patch.object(client, "file_to_base64", side_effect=error):
            expected_error = str(error)  # This will give us the exact format
            with pytest.raises(
                ValueError, match=re.escape(f"Invalid input data: {expected_error}")
            ):
                client.create_embedding(["test.jpg"], task="image")


def test_filter_api_exception(client):
    """Test filter API exception handling"""
    error = ApiException(status=500, reason="Internal Server Error")
    client.filter_api.api_views_filter = MagicMock(side_effect=error)
    with pytest.raises(RuntimeError, match="API Error: 500 - Internal Server Error"):
        client.filter({"key": "test", "value": "test", "lookup": "contains"})


# Add parameterized tests for all API methods that can raise ApiException
@pytest.mark.parametrize(
    "method_name,method_args,api_name,api_method",
    [
        ("get_collection", ["test"], "collections_api", "api_views_get_collection"),
        (
            "create_collection",
            ["test"],
            "collections_api",
            "api_views_create_collection",
        ),
        (
            "partial_update_collection",
            ["test", "new-name", {"key": "value"}],
            "collections_api",
            "api_views_partial_update_collection",
        ),
        ("list_collections", [], "collections_api", "api_views_list_collections"),
        (
            "delete_collection",
            ["test"],
            "collections_api",
            "api_views_delete_collection",
        ),
        ("get_document", ["test"], "documents_api", "api_views_get_document"),
        (
            "upsert_document",
            [
                "test-doc",
                None,
                "test-collection",
                "http://test.url",
            ],  # Keep only this version
            "documents_api",
            "api_views_upsert_document",
        ),
        (
            "partial_update_document",
            ["test", "test", {}],
            "documents_api",
            "api_views_partial_update_document",
        ),
        ("list_documents", [], "documents_api", "api_views_list_documents"),
        (
            "delete_document",
            ["test", "test"],
            "documents_api",
            "api_views_delete_document",
        ),
        ("add_webhook", ["http://test.com"], "webhook_api", "api_views_add_webhook"),
    ],
)
def test_api_methods_error_handling(
    client, method_name, method_args, api_name, api_method
):
    """Test error handling for all API methods"""
    error = ApiException(status=500, reason=f"Error in {method_name}")
    api = getattr(client, api_name)
    setattr(api, api_method, MagicMock(side_effect=error))

    method = getattr(client, method_name)

    # Special handling for upsert_document
    if method_name == "upsert_document":
        kwargs = {
            "name": method_args[0],
            "metadata": method_args[1],
            "collection_name": method_args[2],
            "document_url": method_args[3],
        }
        with pytest.raises(
            RuntimeError, match=f"API Error: 500 - Error in {method_name}"
        ):
            method(**kwargs)
    else:
        with pytest.raises(
            RuntimeError, match=f"API Error: 500 - Error in {method_name}"
        ):
            method(*method_args)


def test_search_api_exception():
    """Test search method when API raises an exception"""
    client = ColiVara(api_key="test-key")
    error = ApiException(status=500, reason="Search Error")
    client.search_api.api_views_search = MagicMock(side_effect=error)

    with pytest.raises(RuntimeError, match="API Error: 500 - Search Error"):
        client.search(
            query="test query",
            collection_name="test-collection",
            query_filter={
                "key": "test",
                "value": "test",
                "lookup": "contains",
                "on": "document",
            },
        )


@pytest.mark.parametrize(
    "secret,payload,headers,expected,description",
    [
        (
            "test_webhook_secret",
            '{"test": 2432232314}',
            {
                "svix-id": "msg_p5jXN8AQM9LWM0D4loKWxJek",
                "svix-timestamp": "1614265330",
                "svix-signature": "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
            },
            True,
            "valid webhook signature",
        ),
        (
            "incorrect-secret",
            "test-payload",
            {"svix-signature": "invalid-signature"},
            False,
            "invalid secret or signature",
        ),
        (
            "test-secret",
            "test-payload",
            {"invalid-header": "value"},
            False,
            "invalid headers",
        ),
        (
            "test-secret",
            "",
            {"svix-signature": "test-signature"},
            False,
            "empty payload",
        ),
    ],
)
def test_validate_webhook_scenarios(
    client, secret, payload, headers, expected, description
):
    """
    Comprehensive test for webhook validation with different scenarios:
    1. Valid webhook signature
    2. Invalid secret or signature
    3. Invalid headers
    4. Empty payload
    """
    if description == "valid webhook signature":
        # Mock webhook verify for valid case
        with patch("colivara_py.client.Webhook") as MockWebhook:
            mock_webhook = MagicMock()
            MockWebhook.return_value = mock_webhook
            mock_webhook.verify.return_value = True
            result = client.validate_webhook(secret, payload, headers)
    elif description == "invalid secret or signature":
        # Mock webhook verify for invalid case
        with patch("svix.webhooks.Webhook.verify", side_effect=Exception("Invalid")):
            result = client.validate_webhook(secret, payload, headers)
    else:
        # Direct validation for other cases
        result = client.validate_webhook(secret, payload, headers)

    assert result == expected, f"Failed for scenario: {description}"


@pytest.mark.parametrize(
    "metadata,expected_metadata",
    [
        ({"key": "value"}, {"key": "value"}),
        (None, {}),
    ],
)
def test_upsert_document_with_metadata(
    client, mock_api_response, metadata, expected_metadata
):
    client.documents_api.api_views_upsert_document = MagicMock(
        return_value=mock_api_response
    )
    result = client.upsert_document(
        name="test-doc",
        collection_name="test-collection",
        document_url="http://test.url",
        metadata=metadata,
    )
    assert result == mock_api_response


# Search Image Tests


def test_search_image_with_path(client, mock_api_response):
    """Test search_image with image path"""
    client.search_api.api_views_search_image = MagicMock(return_value=mock_api_response)

    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("pathlib.Path.resolve", return_value=Path("test.jpg")),
        patch("os.access", return_value=True),
        patch("builtins.open", mock_open(read_data=b"test image content")),
    ):
        result = client.search_image(
            collection_name="test-collection",
            image_path="test.jpg",
            top_k=5,
        )

        assert result == mock_api_response
        client.search_api.api_views_search_image.assert_called_once()
        call_args = client.search_api.api_views_search_image.call_args[0][0]
        assert call_args.img_base64 == base64.b64encode(b"test image content").decode(
            "utf-8"
        )
        assert call_args.collection_name == "test-collection"
        assert call_args.top_k == 5


def test_search_image_with_base64(client, mock_api_response):
    """Test search_image with base64 string"""
    client.search_api.api_views_search_image = MagicMock(return_value=mock_api_response)

    test_base64 = base64.b64encode(b"test image content").decode("utf-8")
    result = client.search_image(
        collection_name="test-collection",
        image_base64=test_base64,
    )

    assert result == mock_api_response
    client.search_api.api_views_search_image.assert_called_once()
    call_args = client.search_api.api_views_search_image.call_args[0][0]
    assert call_args.img_base64 == test_base64
    assert call_args.collection_name == "test-collection"
    assert call_args.top_k == 3  # default value


def test_search_image_with_filter(client, mock_api_response):
    """Test search_image with filter"""
    client.search_api.api_views_search_image = MagicMock(return_value=mock_api_response)

    test_base64 = base64.b64encode(b"test image content").decode("utf-8")
    result = client.search_image(
        collection_name="test-collection",
        image_base64=test_base64,
        query_filter={
            "key": "test",
            "value": "test",
            "lookup": "contains",
            "on": "document",
        },
    )

    assert result == mock_api_response
    client.search_api.api_views_search_image.assert_called_once()
    call_args = client.search_api.api_views_search_image.call_args[0][0]
    # Compare the actual instance value instead of the Key object
    assert call_args.query_filter.key.actual_instance == "test"
    assert call_args.query_filter.value.actual_instance == "test"
    assert call_args.query_filter.lookup.value == "contains"
    assert call_args.query_filter.on.value == "document"


def test_search_image_with_invalid_filter(client):
    """Test search_image with invalid filter"""
    invalid_filter = {
        "key": "test",
        "value": "test",
        "lookup": "invalid",
        "on": "invalid",
    }

    with pytest.raises(Exception) as exc_info:
        client.search_image(
            collection_name="test-collection",
            image_base64="test_base64",
            query_filter=invalid_filter,
        )
    assert "validation errors for QueryFilter" in str(exc_info.value)


def test_search_image_no_input(client):
    """Test search_image with no image input"""
    with pytest.raises(
        ValueError, match="Either image_path or image_base64 must be provided"
    ):
        client.search_image(collection_name="test-collection")


def test_search_image_file_not_found(client):
    """Test search_image with non-existent file"""
    with (
        patch("pathlib.Path.is_file", return_value=False),
        patch("pathlib.Path.resolve", return_value=Path("nonexistent.jpg")),
    ):
        with pytest.raises(
            ValueError, match=r"The specified path is not a file: .*nonexistent\.jpg"
        ):
            client.search_image(
                collection_name="test-collection",
                image_path="nonexistent.jpg",
            )


def test_search_image_no_read_permission(client):
    """Test search_image with file that has no read permission"""
    with (
        patch("pathlib.Path.is_file", return_value=True),
        patch("pathlib.Path.resolve", return_value=Path("test.jpg")),
        patch("os.access", return_value=False),
    ):
        with pytest.raises(
            ValueError,
            match=r"Error reading file: No read permission for file: test\.jpg",
        ):
            client.search_image(
                collection_name="test-collection",
                image_path="test.jpg",
            )


def test_search_image_api_exception(client):
    """Test search_image when API raises an exception"""
    error = ApiException(status=500, reason="Search Error")
    client.search_api.api_views_search_image = MagicMock(side_effect=error)

    with pytest.raises(RuntimeError, match="API Error: 500 - Search Error"):
        client.search_image(
            collection_name="test-collection",
            image_base64="test_base64",
        )
