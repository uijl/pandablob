"""Fixtures for testing."""
import pytest
from mock import Mock, PropertyMock, patch


@pytest.fixture()
def mock_download():
    """Mock downloading an azure blob."""

    def _mock_download(file_name, file_location):
        """Regular fixtures do not allow arguments."""

        with patch("azure.storage.blob.BlobClient", autospec=True) as MockAzureBlob:

            # Mock the returned contend
            mock_content = Mock()
            with open(file_location, "rb") as f:
                mock_content.readall.return_value = f.read()

            # Mock the methods of the BlobServiceClient
            mock_blob_client = Mock()
            mock_blob_client.download_blob.return_value = mock_content

            # Assign mock to BlobServiceClient
            MockAzureBlob = mock_blob_client

            # Mock the returned name
            mock_name = PropertyMock(return_value=file_name)
            type(MockAzureBlob).blob_name = mock_name

            return MockAzureBlob

    return _mock_download


@pytest.fixture()
def mock_upload():
    """Mock uploading to an azure blob."""

    def _mock_upload(file_name):
        """Regular fixtures do not allow arguments."""

        with patch("azure.storage.blob.BlobClient", autospec=True) as MockAzureBlob:

            # Mock the methods of the BlobServiceClient
            mock_blob_client = Mock()
            mock_blob_client.upload_blob

            # Assign mock to BlobServiceClient
            MockAzureBlob = mock_blob_client

            # Mock the returned name
            mock_name = PropertyMock(return_value=file_name)
            type(MockAzureBlob).blob_name = mock_name

            return MockAzureBlob
    
    return _mock_upload