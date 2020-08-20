"""Test downloading a blob and returning a DataFrame."""

import io
from pathlib import Path

import pandas as pd
import pytest
from mock import MagicMock, Mock, PropertyMock, patch

import pandablob

FILES = Path.cwd().joinpath("tests", "test_files")
FILES_IO = Path.cwd().joinpath("tests", "test_io")


def mock_download(mock_azure_blob, file):
    """Mock uploading to the azure blob."""

    # Download blob and make DataFrame
    df = pandablob.blob_to_df(mock_azure_blob)

    # Make DataFrame from original file and compare
    file_location = FILES.joinpath(file)
    extension = file_location.suffix

    # download blob and return DataFrame
    if extension == ".csv" or extension == ".txt":
        compare_df = pd.read_table(file_location)  # , delimiter=",", index_col=0)
        assert df.equals(compare_df)
    if extension == ".json":
        compare_df = pd.read_json(file_location)  # , orient="index")
        assert df.equals(compare_df)
    if extension == ".xlsx" or extension == ".xls":
        compare_df = pd.read_excel(file_location)  # , index_col=0)
        assert df.equals(compare_df)


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
def test_download(file):
    """Test downloading the listed files."""

    with patch("azure.storage.blob.BlobClient", autospec=True) as MockAzureBlob:

        # Mock the returned contend
        mock_content = Mock()
        file_location = FILES.joinpath(file)
        with open(file_location, "rb") as f:
            mock_content.readall.return_value = f.read()

        # Mock the methods of the BlobServiceClient
        mock_blob_client = Mock()
        mock_blob_client.download_blob.return_value = mock_content

        # Assign mock to BlobServiceClient
        MockAzureBlob = mock_blob_client

        # Mock the returned name
        mock_name = PropertyMock(return_value=file)
        type(MockAzureBlob).blob_name = mock_name

        # Run test
        mock_download(MockAzureBlob, file)
