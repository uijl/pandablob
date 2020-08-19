import pytest
from pathlib import Path
import pandas as pd
import io
from mock import Mock, patch
import pandablob

FILES = Path("test_files")
FILES_IO = Path("test_io")


def mock_download(mock_azure_blob, file):
    """Mock uploading to the azure blob."""

    df = pandablob.blob_to_df(mock_azure_blob)


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

        file_location = FILES.joinpath(file)
        extension = file_location.suffix.replace(".", "")

        if extension in ["csv", "json", "txt"]:
            with open(FILES_IO.joinpath(f"{extension}_io"), "r") as f:
                content = io.StringIO(f)
        elif extension in ["xls", "xlsx"]:
            with open(FILES_IO.joinpath(f"{extension}_io"), "rb") as f:
                content = io.BytesIO(f)

        # Mock the returned contend
        mock_content = Mock()
        mock_content.readall.return_value = content

        # Mock the methods of the BlobServiceClient
        mock_blob_client = Mock()
        mock_blob_client.download_blob.return_value = mock_content
        mock_blob_client.blob_name.return_value = file

        # Run test
        mock_download(mock_blob_client, file)
