import pytest
import pandas as pd
from mock import Mock, patch


def mock_upload(mock_azure_blob):
    """Mock uploading to the azure blob."""


@pytest.mark.parametrize(
    "file",
    [
        "test_data.csv",
        "test_data.json",
        "test_data.txt",
        "test_data.xls",
        "test_data.xlsx",
    ],
)
def test_upload(file):
    with patch("azure.storage.blob.BlobServiceClient", autospec=True) as MockAzureBlob:

        # Mock the returned contend
        mock_content = Mock()
        mock_content.readall.return_value = CONTENT

        # Mock the methods of the BlobServiceClient
        mock_blob_client = Mock()
        mock_blob_client.download_blob.return_value = mock_content

        # Assign mocks to BlobServiceClient methods
        mock_blob_service = Mock()
        mock_blob_service.get_container_client.return_value = mock_container_client
        mock_blob_service.get_blob_client.return_value = mock_blob_client

        # Assign mock to BlobServiceClient
        MockAzureBlob.return_value = mock_blob_service

        # Run test
        mock_download(session_factory, AzureBlobStorageProtocol, mock_content.readall)


def test_csv_file():
    """ Test uploading and downloading a .csv file. """

    # Open file

    # Upload file

    # Download file

    # Test
    assert df == downloaded_df


def test_csv_file_kwargs():
    """ Test uploading and downloading a .csv file with given keyword arguments. """

    # Open file

    # Upload file

    # Download file

    # Test
    assert df == downloaded_df
