import os
import requests
from typing import Optional, Dict, Any, List, Union
from .models import CollectionIn, CollectionOut, GenericError, PatchCollectionIn, DocumentIn, DocumentOut, DocumentInPatch
import base64
from pathlib import Path

class Colivara:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initializes the Colivara client.

        Args:
            base_url: The base URL for the API (optional).
            api_key: The API key for authentication (optional).

        Raises:
            ValueError: If the API key is not provided.
        """

        self.base_url = base_url or "https://api.colivara.com"  
        self.api_key = api_key or os.getenv("COLIVARA_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either through parameter or COLIVARA_API_KEY environment variable.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_collection(self, name: str, metadata: Optional[Dict[str, Any]] = {}) -> CollectionOut:
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


    def partial_update_collection(self, collection_name: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> CollectionOut:
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
    
    
    def upsert_document(self, 
                        name: str, 
                        metadata: Optional[Dict[str, Any]] = None, 
                        collection_name: str = "default collection", 
                        document_url: Optional[str] = None, 
                        document_base64: Optional[str] = None,
                        document_path: Optional[Union[str, Path]] = None
                        ) -> DocumentOut:
        """
        Create or update a document in a collection.

        This method allows you to upsert (insert or update) a document in the specified collection.
        You can provide either a URL or a base64-encoded string of the document content.

        Args:
            name (str): The name of the document.
            metadata (Optional[Dict[str, Any]]): Additional metadata for the document.
            collection_name (str): The name of the collection to add the document to. Defaults to "default collection".
            document_url (Optional[str]): The URL of the document, if available.
            document_base64 (Optional[str]): The base64-encoded string of the document content, if available.
            document_path (Optional[str]): The path to the document file to be uploaded.
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
                raise FileNotFoundError(f"The specified file does not exist: {document_path}")
            except Exception as e:
                raise ValueError(f"Error reading file: {str(e)}")
        if not document_url and not document_base64:
            raise ValueError("Either document_url, document_base64, or document_path must be provided.")

        request_url = f"{self.base_url}/v1/documents/upsert-document/"
        payload = DocumentIn(
            name=name,
            metadata=metadata or {},
            collection_name=collection_name,
            url=document_url,
            base64=document_base64
        ).model_dump()

        response = requests.post(request_url, json=payload, headers=self.headers)

        if response.status_code == 201:
            return DocumentOut(**response.json())
        elif response.status_code == 400:
            error = GenericError(**response.json())
            raise ValueError(f"Bad request: {error.detail}")
        else:
            response.raise_for_status()