import base64
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from pydantic import ValidationError
from svix.webhooks import Webhook

from .models import (
    CollectionIn,
    CollectionOut,
    DocumentIn,
    DocumentInPatch,
    DocumentOut,
    EmbeddingsIn,
    EmbeddingsOut,
    FileOut,
    GenericError,
    GenericMessage,
    PatchCollectionIn,
    QueryFilter,
    QueryIn,
    QueryOut,
    TaskEnum,
    WebhookOut,
)


class ColiVara:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initializes the ColiVara client.

        Args:
            base_url: The base URL for the API (optional).
            api_key: The API key for authentication (optional).

        Raises:
            ValueError: If the API key is not provided.
        """

        self.base_url = base_url or "https://api.colivara.com"
        self.api_key = api_key or os.getenv("COLIVARA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either through parameter or COLIVARA_API_KEY environment variable."
            )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_collection(
        self, name: str, metadata: Optional[Dict[str, Any]] = {}
    ) -> CollectionOut:
        """
        Creates a new collection.

        Args:
            name: The name of the new collection.
            metadata: The metadata for the new collection (optional).

        Returns:
            The created CollectionOut object.

        Raises:
            Exception: If there's a conflict or an unexpected error occurs.
        """

        url = f"{self.base_url}/v1/collections/"
        payload = CollectionIn(name=name, metadata=metadata).model_dump()
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 201:
            return CollectionOut(**response.json())
        elif response.status_code == 409:
            error = GenericError(**response.json())
            raise Exception(f"Conflict error: {error.detail}")
        else:
            response.raise_for_status()

    def list_collections(self) -> List[CollectionOut]:
        """
        Lists all collections.

        Returns:
            A list of CollectionOut objects.

        Raises:
            ValueError: If the response format is unexpected.
            Exception: If an unexpected error occurs.
        """

        url = f"{self.base_url}/v1/collections/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        if response.status_code == 200:
            collections_data = response.json()
            # Handle potential empty list
            if isinstance(collections_data, list):
                return [CollectionOut(**collection) for collection in collections_data]
            else:
                raise ValueError(f"Unexpected response format: {collections_data}")
        else:
            response.raise_for_status()

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

        url = f"{self.base_url}/v1/collections/{collection_name}/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return CollectionOut(**response.json())
        elif response.status_code == 404:
            raise Exception(f"Collection '{collection_name}' not found.")
        else:
            response.raise_for_status()

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

        url = f"{self.base_url}/v1/collections/{collection_name}/"

        # Create a CollectionIn object with sane defaults and only updated fields
        updated_data = PatchCollectionIn(name=name, metadata=metadata)

        payload = updated_data.model_dump()
        response = requests.patch(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return CollectionOut(**response.json())
        elif response.status_code == 404:
            raise Exception(f"Collection '{collection_name}' not found.")
        else:
            response.raise_for_status()

    def delete_collection(self, collection_name: str) -> None:
        """
        Deletes a specific collection.

        Args:
            collection_name: The name of the collection to delete.

        Raises:
            Exception: If the collection is not found or an unexpected error occurs.
        """

        url = f"{self.base_url}/v1/collections/{collection_name}/"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return
        elif response.status_code == 404:
            raise Exception(f"Collection '{collection_name}' not found.")
        else:
            response.raise_for_status()

    def add_webhook(
        self,
        url: str,
    ) -> WebhookOut:
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
        request_url = f"{self.base_url}/v1/webhook/"
        payload = {"url": url}

        response = requests.post(request_url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return WebhookOut(**response.json())
        elif response.status_code == 400:
            error = GenericError(**response.json())
            raise ValueError(f"Bad request: {error.detail}")
        else:
            response.raise_for_status()

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

    def upsert_document(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        collection_name: str = "default_collection",
        document_url: Optional[str] = None,
        document_base64: Optional[str] = None,
        document_path: Optional[Union[str, Path]] = None,
        wait: Optional[bool] = False,
    ) -> DocumentOut | GenericMessage:
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
        # if user sent us a document_path, we will read the file and convert it to base64
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

        request_url = f"{self.base_url}/v1/documents/upsert-document/"
        payload = DocumentIn(
            name=name,
            metadata=metadata or {},
            collection_name=collection_name,
            url=document_url,
            base64=document_base64,
            wait=wait,
        ).model_dump()

        response = requests.post(request_url, json=payload, headers=self.headers)

        if response.status_code == 201:
            return DocumentOut(**response.json())
        elif response.status_code == 202:
            status = GenericMessage(**response.json())
            return status
        elif response.status_code == 400:
            error = GenericError(**response.json())
            raise ValueError(f"Bad request: {error.detail}")
        else:
            response.raise_for_status()

    def get_document(
        self,
        document_name: str,
        collection_name: str = "default_collection",
        expand: Optional[str] = None,
    ) -> DocumentOut:
        """
        Retrieve a specific document from the user documents.

        Args:
            document_name (str): The name of the document to retrieve.
            collection_name (str): The name of the collection containing the document.
                                   Defaults to "default_collection".
            expand (Optional[str]): A comma-separated list of fields to expand in the response.
                                    Currently, only "pages" is supported, the document's pages will be included if provided.

        Returns:
            DocumentOut: The retrieved document with its details.

        Raises:
            requests.HTTPError: If the API request fails.
            ValueError: If the document or collection is not found.
        """
        request_url = f"{self.base_url}/v1/documents/{document_name}/"
        params = {"collection_name": collection_name, "expand": expand}

        response = requests.get(request_url, params=params, headers=self.headers)

        if response.status_code == 200:
            return DocumentOut(**response.json())
        elif response.status_code == 404:
            error = GenericError(**response.json())
            raise ValueError(f"Document not found: {error.detail}")
        else:
            response.raise_for_status()

    def partial_update_document(
        self,
        document_name: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        collection_name: Optional[str] = None,
        document_url: Optional[str] = None,
        document_base64: Optional[str] = None,
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

        Returns:
            DocumentOut: The updated document with its details.

        Raises:
            requests.HTTPError: If the API request fails.
            ValueError: If the document is not found or the update is invalid.
        """
        request_url = f"{self.base_url}/v1/documents/{document_name}/"
        payload = DocumentInPatch(
            name=name,
            metadata=metadata,
            collection_name=collection_name,
            url=document_url,
            base64=document_base64,
        ).model_dump(exclude_none=True)

        response = requests.patch(request_url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return DocumentOut(**response.json())
        elif response.status_code in [404, 409]:
            error = GenericError(**response.json())
            raise ValueError(f"Update failed: {error.detail}")
        else:
            response.raise_for_status()

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
        request_url = f"{self.base_url}/v1/documents/"
        params = {"collection_name": collection_name, "expand": expand}

        response = requests.get(request_url, params=params, headers=self.headers)

        if response.status_code == 200:
            return [DocumentOut(**doc) for doc in response.json()]
        else:
            response.raise_for_status()

    def delete_document(
        self, document_name: str, collection_name: str = "default_collection"
    ) -> None:
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
        request_url = f"{self.base_url}/v1/documents/delete-document/{document_name}/"
        params = {"collection_name": collection_name}

        response = requests.delete(request_url, params=params, headers=self.headers)

        if response.status_code == 204:
            return
        elif response.status_code in [404, 409]:
            error = GenericError(**response.json())
            raise ValueError(f"Deletion failed: {error.detail}")
        else:
            response.raise_for_status()

    def search(
        self,
        query: str,
        collection_name: str = "all",
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
        request_url = f"{self.base_url}/v1/search/"
        payload = {
            "query": query,
            "collection_name": collection_name,
            "top_k": top_k,
        }
        filter_obj = None
        if query_filter:
            try:
                filter_obj = QueryFilter(**query_filter)
                payload["query_filter"] = filter_obj.model_dump()
            except ValidationError as e:
                raise ValueError(f"Invalid query_filter: {str(e)}")

        query_in = QueryIn(**payload)  # type: ignore

        response = requests.post(
            request_url, json=query_in.model_dump(), headers=self.headers
        )

        if response.status_code == 200:
            return QueryOut(**response.json())
        elif response.status_code == 503:
            error = GenericError(**response.json())
            raise ValueError(f"Service unavailable: {error.detail}")
        else:
            response.raise_for_status()

    def filter(
        self,
        query_filter: Dict[str, Any],
        expand: Optional[str] = None,
    ) -> List[Union[DocumentOut, CollectionOut]]:
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

        request_url = f"{self.base_url}/v1/filter/"

        try:
            filter_obj = QueryFilter(**query_filter)
            payload = filter_obj.model_dump()
        except ValidationError as e:
            raise ValueError(f"Invalid query_filter: {str(e)}")

        params = {"expand": expand}

        response = requests.post(
            request_url, json=payload, params=params, headers=self.headers
        )

        if response.status_code == 200:
            if query_filter["on"] == "document":
                return [DocumentOut(**doc) for doc in response.json()]
            else:
                return [CollectionOut(**col) for col in response.json()]
        elif response.status_code == 503:
            error = GenericError(**response.json())
            raise ValueError(f"Service unavailable: {error.detail}")
        else:
            response.raise_for_status()

    def file_to_imgbase64(self, file_path: str) -> List[FileOut]:
        """
        Converts a file to a list of base64 encoded images.

        Args:
            file_path: The path to the file to be converted.

        Returns:
            A list of FileOut objects containing the base64 encoded strings of the images.

        Raises:
            Exception: If there's an error during the file conversion process.
        """
        url = f"{self.base_url}/v1/helpers/file-to-imgbase64/"

        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(
                url, files=files, headers={"Authorization": f"Bearer {self.api_key}"}
            )

        if response.status_code == 200:
            return [FileOut(**item) for item in response.json()]
        else:
            response.raise_for_status()

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

    def create_embedding(
        self,
        input_data: Union[str, List[str]],
        task: Union[str, TaskEnum] = TaskEnum.query,
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
        url = f"{self.base_url}/v1/embeddings/"

        # Ensure input_data is a list
        if isinstance(input_data, str):
            input_data = [input_data]

        # Validate and convert task to TaskEnum
        if isinstance(task, str):
            try:
                task = TaskEnum(task.lower())
            except ValueError:
                raise ValueError(f"Invalid task: {task}. Must be 'query' or 'image'.")
        elif not isinstance(task, TaskEnum):
            raise ValueError("Task must be a string or TaskEnum.")

        try:
            # if the task is in image, and we got a path, we will convert the file to base64
            if task == TaskEnum.image:
                for i, d in enumerate(input_data):
                    if Path(d).is_file():
                        input_data[i] = self.file_to_base64(d)
            payload = EmbeddingsIn(input_data=input_data, task=task).model_dump()
        except ValidationError as e:
            raise ValueError(f"Invalid input data: {str(e)}")

        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            return EmbeddingsOut(**data)
        elif response.status_code == 503:
            error = GenericError(**response.json())
            raise Exception(f"Service Unavailable: {error.detail}")
        else:
            response.raise_for_status()
