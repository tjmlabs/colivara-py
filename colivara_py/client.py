import os
from typing import Any, Dict, List, Optional, Union, cast
import base64
from svix.webhooks import Webhook

from colivara_py.api.collections_api import CollectionsApi
from colivara_py.api.documents_api import DocumentsApi
from colivara_py.api.embeddings_api import EmbeddingsApi
from colivara_py.api.filter_api import FilterApi
from colivara_py.api.health_api import HealthApi
from colivara_py.api.helpers_api import HelpersApi
from colivara_py.api.search_api import SearchApi
from colivara_py.api.webhook_api import WebhookApi
from colivara_py.configuration import Configuration
from colivara_py.api_client import ApiClient
from colivara_py.exceptions import ApiException

from colivara_py.models import (
    QueryFilter,
    Key,
    Value,
    FileOut,
    EmbeddingsOut,
    CollectionOut,
    PatchCollectionIn,
    WebhookOut,
    DocumentOut,
    GenericMessage,
    TaskEnum,
    DocumentIn,
    CollectionIn,
    QueryIn,
    DocumentInPatch,
    WebhookIn,
    EmbeddingsIn,
    QueryOut,
    SearchImageIn,
    SearchImageOut,
)

from pathlib import Path
from pydantic import StrictStr


class ColiVara:
    """
    ColiVara SDK Wrapper Class

    A user-friendly wrapper for interacting with the ColiVara API.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: str = "https://api.colivara.com"
    ):
        """
        Initialize the ColiVara SDK.

        :param api_key: API key for authentication. Defaults to the COLIVARA_API_KEY environment variable.
        :param base_url: Base URL of the API.
        """
        self.api_key = api_key or os.getenv("COLIVARA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set in the COLIVARA_API_KEY environment variable."
            )

        # Custom Configuration
        self.config = Configuration(host=base_url)
        self.config.verify_ssl = False
        self.api_client = ApiClient(self.config)

        # Explicitly add Authorization header
        self.api_client.default_headers["Authorization"] = f"Bearer {self.api_key}"

        # Initialize all API modules
        self.collections_api = CollectionsApi(self.api_client)
        self.documents_api = DocumentsApi(self.api_client)
        self.embeddings_api = EmbeddingsApi(self.api_client)
        self.filter_api = FilterApi(self.api_client)
        self.health_api = HealthApi(self.api_client)
        self.helpers_api = HelpersApi(self.api_client)
        self.search_api = SearchApi(self.api_client)
        self.webhook_api = WebhookApi(self.api_client)

    def get_collection(self, collection_name: str) -> CollectionOut:
        """
        Gets a specific collection.

        Args:
            collection_name: The name of the collection to get.

        Returns:
            The requested CollectionOut object.

        Raises:
            Exception: If the collection is not found or an unexpected error occurs.
        """
        try:
            return self.collections_api.api_views_get_collection(collection_name)
        except ApiException as e:
            self._handle_error(e)

    def create_collection(
        self, name: str, metadata: Optional[Dict[str, Any]] = None
    ) -> CollectionOut:
        """
        Create a new collection.

        :param name: Name of the collection.
        :param metadata: Optional metadata for the collection.
        :return: Response from the API.
        """
        body = CollectionIn(name=name, metadata=metadata or {})
        try:
            return self.collections_api.api_views_create_collection(body)
        except ApiException as e:
            self._handle_error(e)

    def partial_update_collection(
        self,
        collection_name: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CollectionOut:
        """
        Partially updates a collection.

        Args:
            collection_name: The name of the collection to update.
            new_name: The new name for the collection (optional).
            new_metadata: The new metadata for the collection (optional).

        Returns:
            The updated CollectionOut object.

        Raises:
            Exception: If the collection is not found or there's a problem with the update.
        """
        body = PatchCollectionIn(name=name, metadata=metadata)
        try:
            return self.collections_api.api_views_partial_update_collection(
                collection_name, body
            )
        except ApiException as e:
            self._handle_error(e)

    def list_collections(self) -> List[CollectionOut]:
        """
        Lists all collections.

        Returns:
            A list of CollectionOut objects.

        Raises:
            ValueError: If the response format is unexpected.
            Exception: If an unexpected error occurs.
        """
        try:
            return self.collections_api.api_views_list_collections()
        except ApiException as e:
            self._handle_error(e)

    def delete_collection(self, collection_name: str) -> None:
        """
        Deletes a specific collection.

        Args:
            collection_name: The name of the collection to delete.

        Raises:
            Exception: If the collection is not found or an unexpected error occurs.
        """
        try:
            return self.collections_api.api_views_delete_collection(collection_name)
        except ApiException as e:
            self._handle_error(e)

    def upsert_document(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        collection_name: str = "default_collection",
        document_url: Optional[str] = None,
        document_base64: Optional[str] = None,
        document_path: Optional[Union[str, Path]] = None,
        wait: Optional[bool] = False,
        use_proxy: Optional[bool] = False,
    ) -> Union[DocumentOut, GenericMessage]:
        """
        Create or update a document in a collection.

        This method allows you to upsert (insert or update) a document in the specified collection.
        You can provide either a URL or a base64-encoded string of the document content.

        Args:
            name (str): The name of the document.
            metadata (Optional[Dict[str, Any]]): Additional metadata for the document.
            collection_name (str): The name of the collection to add the document to. Defaults to "default_collection".
            document_url (Optional[str]): The URL of the document, if available.
            document_base64 (Optional[str]): The base64-encoded string of the document content, if available.
            document_path (Optional[str]): The path to the document file to be uploaded.
            wait (Optional[bool]): If True, the method will wait for the document to be processed before returning.
        Returns:
            DocumentOut: The created or updated document with its details.

        Raises:
            ValueError: If no valid document source is provided or if the file path is invalid.
            FileNotFoundError: If the specified file path does not exist.
            PermissionError: If there's no read permission for the specified file.
            requests.HTTPError: If the API request fails.
        """
        if document_path:
            try:
                path = Path(document_path).resolve()
                if not path.is_file():
                    raise ValueError(f"The specified path is not a file: {path}")
                if not os.access(path, os.R_OK):
                    raise PermissionError(f"No read permission for file: {path}")
                with open(path, "rb") as file:
                    document_base64 = base64.b64encode(file.read()).decode("utf-8")
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"The specified file does not exist: {document_path}"
                )
            except Exception as e:
                raise ValueError(f"Error reading file: {str(e)}")
        if not document_url and not document_base64:
            raise ValueError(
                "Either document_url, document_base64, or document_path must be provided."
            )
        body = DocumentIn(
            name=name,
            metadata=metadata or {},
            collection_name=collection_name,
            url=document_url,
            base64=document_base64,
            wait=wait,
            use_proxy=use_proxy,
        )
        try:
            return self.documents_api.api_views_upsert_document(body)
        except ApiException as e:
            self._handle_error(e)

    def get_document(
        self,
        document_name: str,
        collection_name: Optional[str] = None,
        expand: Optional[StrictStr] = None,
    ) -> DocumentOut:
        """
        Retrieve a specific document from the user documents.

        Args:
            document_name (str): The name of the document to retrieve.
            collection_name (Optional[str]): The name of the collection containing the document.
                             Defaults to None.
            expand (Optional[str]): A comma-separated list of fields to expand in the response.
                        Currently, only "pages" is supported, the document's pages will be included if provided.

        Returns:
            DocumentOut: The retrieved document with its details.

        Raises:
            requests.HTTPError: If the API request fails.
            ValueError: If the document or collection is not found.
        """
        try:
            return self.documents_api.api_views_get_document(
                document_name, collection_name, expand
            )
        except ApiException as e:
            self._handle_error(e)

    def partial_update_document(
        self,
        document_name: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        collection_name: Optional[str] = None,
        document_url: Optional[str] = None,
        document_base64: Optional[str] = None,
        use_proxy: Optional[bool] = False,
    ) -> DocumentOut:
        """
        Partially update a document.

        This method allows for partial updates to a document's details. Only the fields provided will be updated.

        Args:
            document_name (str): The name of the document to be updated.
            name (Optional[str]): The new name for the document, if changing.
            metadata (Optional[Dict[str, Any]]): Updated metadata for the document.
            collection_name (Optional[str]): The name of the collection to move the document to, if changing.
            document_url (Optional[str]): The new URL of the document, if changing.
            document_base64 (Optional[str]): The new base64-encoded string of the document content, if changing.
            use_proxy (Optional[bool]): Whether to use a proxy for the document URL.

        Returns:
            DocumentOut: The updated document with its details.

        Raises:
            requests.HTTPError: If the API request fails.
            ValueError: If the document is not found or the update is invalid.
        """
        body = DocumentInPatch(
            name=name,
            metadata=metadata,
            collection_name=collection_name,
            url=document_url,
            base64=document_base64,
            use_proxy=use_proxy,
        )
        try:
            return self.documents_api.api_views_partial_update_document(
                document_name, body
            )
        except ApiException as e:
            self._handle_error(e)

    def list_documents(
        self, collection_name: str = "default_collection", expand: Optional[str] = None
    ) -> List[DocumentOut]:
        """
        Fetch a list of documents for a given collection.

        Args:
            collection_name (str): The name of the collection to fetch documents from.
                                   Defaults to "default_collection". Use "all" to fetch documents from all collections.
            expand (Optional[str]): A comma-separated string specifying additional fields to include in the response.
                                    If "pages" is included, the pages of each document will be included.

        Returns:
            List[DocumentOut]: A list of documents with their details.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        try:
            return self.documents_api.api_views_list_documents(
                collection_name=collection_name, expand=expand
            )
        except ApiException as e:
            self._handle_error(e)

    def delete_document(self, document_name: str, collection_name: str) -> None:
        """
        Delete a document by its name.

        Args:
            document_name (str): The name of the document to be deleted.
            collection_name (str): The name of the collection containing the document.
                                   Defaults to "default_collection". Use "all" to access all collections belonging to the user.

        Raises:
            requests.HTTPError: If the API request fails.
            ValueError: If the document does not exist or does not belong to the authenticated user.
        """
        try:
            return self.documents_api.api_views_delete_document(
                document_name, collection_name
            )
        except ApiException as e:
            self._handle_error(e)

    def filter(
        self, query_filter: Dict[str, Any], expand: Optional[str] = None
    ) -> list[CollectionOut] | list[DocumentOut] | None:
        """
        Filter for documents and collections that meet the criteria of the filter.

        Args:
            query_filter (Dict[str, Any]): A dictionary specifying the filter criteria.
                The filter can be used to narrow down the search based on specific criteria.
                The dictionary should contain the following keys:
                - "on": "document" or "collection"
                - "key": str or List[str]
                - "value": Optional[Union[str, int, float, bool]]
                - "lookup": One of "key_lookup", "contains", "contained_by", "has_key", "has_keys", "has_any_keys"
            expand (Optional[str]): A comma-separated list of fields to expand in the response.
                Currently, only "pages" is supported, the document's pages will be included if provided.


        Returns:
            DocumentOut: The retrieved documents with their details.
            CollectionOut: The retrieved collections with their details.

        Raises:
            ValueError: If the query_filter is invalid.
            requests.HTTPError: If the API request fails.

        Example:
            # Simple filter
            results = client.filter({
                "on": "document",
                "key": "category",
                "value": "AI",
                "lookup": "contains"
            })

            # Filter with a list of keys
            results = client.filter({
                "on": "collection",
                "key": ["tag1", "tag2"],
                "lookup": "has_keys"
            })
        """
        try:
            filter_key = Key(query_filter["key"])
            filter_value = Value(query_filter["value"])
            filter_lookup = query_filter["lookup"]
            on = query_filter.get("on", "document")

            filter_model = QueryFilter(
                key=filter_key, value=filter_value, lookup=filter_lookup, on=on
            )

            result = self.filter_api.api_views_filter(
                query_filter=filter_model, expand=expand
            )

            # Return the actual instance instead of the Response object
            return result.actual_instance

        except ApiException as e:
            # Handle any API exceptions and pass them to a custom error handler
            self._handle_error(e)
        except KeyError as e:
            # Handle missing keys in the query_filter dictionary
            raise ValueError(f"Missing required key: {e}")
        except Exception as e:
            # General exception handling
            raise Exception(f"An unexpected error occurred: {e}")

    def file_to_base64(self, file_path: str) -> str:
        """
        Converts a file to a base64 encoded string.

        Args:
            file_path: The path to the file to be converted.

        Returns:
            A base64 encoded string of the file.

        Raises:
            Exception: If there's an error during the file conversion process.
        """
        # Read the file
        with open(file_path, "rb") as file:
            file_content = file.read()
        # Encode the file content to base64
        base64_content = base64.b64encode(file_content).decode("utf-8")
        return base64_content

    def file_to_imgbase64(self, file_path: str) -> List[FileOut]:
        """
        Convert a file to base64-encoded strings for its image representations.

        :param file_path: Path to the file to be converted.
        :return: A list of FileOut objects containing base64-encoded strings of images.
        """
        with open(file_path, "rb") as file:
            file_content = file.read()

        try:
            # The response is already a List[FileOut], so we can return it directly
            response = self.helpers_api.api_views_file_to_imgbase64(file_content)
            return response
        except ApiException as e:
            self._handle_error(e)

    def search(
        self,
        query: str,
        collection_name: str,
        top_k: int = 3,
        query_filter: Optional[Dict[str, Any]] = None,
    ) -> QueryOut:
        """
        Search for pages similar to a given query.

        This method allows you to search for pages similar to a given query across all documents
        in the specified collection.

        Args:
            query (str): The search query string.
            collection_name (str): The name of the collection to search in. Defaults to "all".
            top_k (int): The number of top results to return. Defaults to 3.
            query_filter (Optional[Dict[str, Any]]): An optional filter to apply to the search results.
                The filter can be used to narrow down the search based on specific criteria.
                It should be a dictionary with the following possible keys:
                - "on": "document" or "collection"
                - "key": str or List[str]
                - "value": Optional[Union[str, int, float, bool]]
                - "lookup": One of "key_lookup", "contains", "contained_by", "has_key", "has_keys", "has_any_keys"

        Returns:
            QueryOut: The search results, including the query and a list of similar pages.

        Raises:
            ValueError: If the query is invalid, the collection does not exist, or the query_filter is invalid.
            requests.HTTPError: If the API request fails.

        Examples:
            # Simple search
            results = client.search("what is 1+1?")

            # search with a specific collection
            results = client.search("what is 1+1?", collection_name="my_collection")

            # Search with a filter on document metadata
            results = client.search("what is 1+1?", query_filter={
                "on": "document",
                "key": "category",
                "value": "AI",
                "lookup": "contains"
            })

            # Search with a filter on collection metadata
            results = client.search("what is 1+1?", query_filter={
                "on": "collection",
                "key": ["tag1", "tag2"],
                "lookup": "has_any_keys"
            })
        """
        query_filter_obj = None
        if query_filter:
            filter_key = Key(query_filter["key"])
            filter_value = Value(query_filter["value"])
            filter_lookup = query_filter["lookup"]
            on = query_filter.get("on", "document")

            query_filter_obj = QueryFilter(
                key=filter_key, value=filter_value, lookup=filter_lookup, on=on
            )

        body = QueryIn(
            query=query,
            collection_name=collection_name,
            top_k=top_k,
            query_filter=query_filter_obj,
        )
        try:
            return self.search_api.api_views_search(body)
        except ApiException as e:
            self._handle_error(e)

    def search_image(
        self,
        collection_name: str,
        image_path: Optional[Union[str, Path]] = None,
        image_base64: Optional[str] = None,
        top_k: int = 3,
        query_filter: Optional[Dict[str, Any]] = None,
    ) -> SearchImageOut:
        """
        Search for pages similar to a given image.

        This method allows you to search for pages similar to a given image across all documents
        in the specified collection. You can provide either a path to an image file or a base64-encoded
        string of the image content.

        Args:
            collection_name (str): The name of the collection to search in.
            image_path (Optional[Union[str, Path]]): Path to the image file to search with.
            image_base64 (Optional[str]): Base64-encoded string of the image content.
            top_k (int): The number of top results to return. Defaults to 3.
            query_filter (Optional[Dict[str, Any]]): An optional filter to apply to the search results.
                The filter can be used to narrow down the search based on specific criteria.
                It should be a dictionary with the following possible keys:
                - "on": "document" or "collection"
                - "key": str or List[str]
                - "value": Optional[Union[str, int, float, bool]]
                - "lookup": One of "key_lookup", "contains", "contained_by", "has_key", "has_keys", "has_any_keys"

        Returns:
            SearchImageOut: The search results, including a list of similar pages.

        Raises:
            ValueError: If neither image_path nor image_base64 is provided, or if the image file can't be read.
            FileNotFoundError: If the specified image file does not exist.
            PermissionError: If there's no read permission for the specified file.
            ApiException: If the API request fails.

        Examples:
            # Search with image file
            results = client.search_image("my_collection", image_path="path/to/image.jpg")

            # Search with base64-encoded image
            results = client.search_image("my_collection", image_base64="base64_encoded_string")

            # Search with filter
            results = client.search_image(
                "my_collection",
                image_path="path/to/image.jpg",
                query_filter={
                    "on": "document",
                    "key": "category",
                    "value": "landscape",
                    "lookup": "contains"
                }
            )
        """
        # Handle image input
        img_base64 = image_base64
        if image_path:
            try:
                path = Path(image_path).resolve()
                if not path.is_file():
                    raise ValueError(f"The specified path is not a file: {path}")
                if not os.access(path, os.R_OK):
                    raise PermissionError(f"No read permission for file: {path}")
                with open(path, "rb") as file:
                    img_base64 = base64.b64encode(file.read()).decode("utf-8")
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"The specified file does not exist: {image_path}"
                )
            except Exception as e:
                raise ValueError(f"Error reading file: {str(e)}")

        if not img_base64:
            raise ValueError("Either image_path or image_base64 must be provided.")

        # Handle query filter
        query_filter_obj = None
        if query_filter:
            filter_key = Key(query_filter["key"])
            filter_value = Value(query_filter["value"])
            filter_lookup = query_filter["lookup"]
            on = query_filter.get("on", "document")

            query_filter_obj = QueryFilter(
                key=filter_key, value=filter_value, lookup=filter_lookup, on=on
            )

        # Create search request body
        body = SearchImageIn(
            img_base64=img_base64,
            collection_name=collection_name,
            top_k=top_k,
            query_filter=query_filter_obj,
        )

        try:
            return self.search_api.api_views_search_image(body)
        except ApiException as e:
            self._handle_error(e)

    def create_embedding(
        self,
        input_data: Union[str, List[str]],
        task: Union[str, TaskEnum] = TaskEnum.QUERY,
    ) -> EmbeddingsOut:
        """
        Creates embeddings for the given input data.

        Args:
            input_data: A string or list of strings to create embeddings for.
            task: The task type for embedding creation. Can be "query" or "image". Defaults to "query".

        Returns:
            An EmbeddingsOut object containing the embeddings, model information, and usage data.

        Raises:
            ValueError: If an invalid task is provided.
            Exception: If there's an unexpected error from the API.

        Example:
            client.create_embedding("what is 1+1?", task="query")
            client.create_embedding(["image1.jpg", "image2.jpg"], task="image")
        """
        if isinstance(input_data, str):
            input_data = [input_data]

        # Validate and convert task to TaskEnum
        if isinstance(task, str):
            try:
                task = TaskEnum(task.lower())
            except ValueError:
                raise ValueError(f"Invalid task: {task}. Must be 'query' or 'image'.")
        try:
            # if the task is in image, and we got a path, we will convert the file to base64
            if task == TaskEnum.IMAGE:
                for i, d in enumerate(input_data):
                    if Path(d).is_file():
                        input_data[i] = self.file_to_base64(d)
        except ApiException as e:
            raise ValueError(f"Invalid input data: {str(e)}")

        body = EmbeddingsIn(input_data=input_data, task=task)
        try:
            return self.embeddings_api.api_views_embeddings(body)
        except ApiException as e:
            self._handle_error(e)

    def add_webhook(self, url: str) -> WebhookOut:
        """
        Add a webhook to the service.

        This endpoint allows the user to add a webhook to the service. The webhook will be called when a document is upserted
        with the upsertion status.

        Events are document upsert successful, document upsert failed.

        Args:
            url: The URL of the webhook to be added.

        Returns:
            WebhookOut: The added webhook endpoint id, associated app id, and webhook secret.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        body = WebhookIn(url=url)
        try:
            return self.webhook_api.api_views_add_webhook(body)
        except ApiException as e:
            self._handle_error(e)

    def validate_webhook(
        self, webhook_secret: str, payload: str, headers: Dict[str, Any]
    ) -> bool:
        """
        Validates a webhook request.

        This endpoint allows the user to validate a webhook request given the webhook secret, payload, and headers.

        Args:
            webhook_secret: The webhook secret to validate the request.
            payload: The payload of the webhook request.
            headers: The headers of the webhook request.

        Returns:
            bool: True if the request is valid, False otherwise
        """
        try:
            wh = Webhook(webhook_secret)
            wh.verify(payload, headers)
            return True
        except Exception:
            return False

    def check_health(self) -> None:
        """
        Check the health of the API.

        :return: Health status of the API.
        """
        try:
            return self.health_api.api_views_health()
        except ApiException as e:
            self._handle_error(e)

    def _handle_error(self, error: ApiException):
        """
        Handle API exceptions.

        :param error: The API exception to handle.
        :raise: Re-raises the error with additional context.
        """
        error_message = f"API Error: {error.status} - {error.reason}"
        if hasattr(error, "body") and error.body:
            body = cast(Union[str, bytes], error.body)
            error_message += f"\nResponse Body: {body.decode('utf-8') if isinstance(body, bytes) else body}"
        if hasattr(error, "status") and error.status:
            if error.status == 400:
                error_message += "\nBad Request: The server could not understand the request due to invalid syntax."
            elif error.status == 401:
                error_message += (
                    "\nUnauthorized: Access is denied due to invalid credentials."
                )
            elif error.status == 403:
                error_message += (
                    "\nForbidden: You do not have permission to access this resource."
                )
            elif error.status == 404:
                error_message += (
                    "\nNot Found: The requested resource could not be found."
                )
            elif error.status == 409:
                error_message += "\nConflict: The request could not be completed due to a conflict with the current state of the resource."
            elif error.status == 429:
                error_message += "\nToo Many Requests: You have sent too many requests in a given amount of time."
            elif error.status == 500:
                error_message += "\nInternal Server Error: The server encountered an unexpected condition."
            elif error.status == 503:
                error_message += "\nService Unavailable: The server is not ready to handle the request."
            else:
                error_message += f"\nUnexpected Error: {error.status}"
        raise RuntimeError(error_message) from error
