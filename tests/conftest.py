"""Fixtures for testing."""

from pathlib import Path

import pytest
from mock import Mock, PropertyMock, patch


@pytest.fixture()
def test_files():
    """Return the directory with the files for testing."""

    return Path.cwd().joinpath("tests", "test_files")


# @pytest.fixture()
# def test_files_io():
#     """Return the directory with the files for testing."""

#     return_dict = {}
#     file_path = Path.cwd().joinpath("tests", "test_io")
#     with open(file_path.joinpath("csv_io"), "rt") as f:
#         return_dict.update({"csv": f.read()})
#     with open(file_path.joinpath("txt_io"), "rt") as f:
#         return_dict.update({"txt": f.read()})
#     with open(file_path.joinpath("json_io"), "rt") as f:
#         return_dict.update({"json": f.read()})
#     with open(file_path.joinpath("xls_io"), "rb") as f:
#         return_dict.update({"xls": f.read()})
#     with open(file_path.joinpath("xlsx_io"), "rb") as f:
#         return_dict.update({"xlsx": f.read()})

#     return return_dict


@pytest.fixture()
def pandas_arguments():
    """Return a dict with the keyword arguments for pandas."""

    return {
        "csv": {"delimiter": ",", "index_col": 0},
        "json": {"orient": "index"},
        "txt": {"delimiter": ",", "index_col": 0},
        "xls": {"index_col": 0},
        "xlsx": {"index_col": 0},
    }


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

            # Assign mock to BlobServiceClient
            mock_blob_client = Mock()
            MockAzureBlob = mock_blob_client

            # Mock the returned name
            mock_name = PropertyMock(return_value=file_name)
            type(MockAzureBlob).blob_name = mock_name

            return MockAzureBlob

    return _mock_upload
