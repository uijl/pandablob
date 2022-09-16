"""Fixtures for testing."""

import io
from pathlib import Path
from unittest.mock import Mock, PropertyMock, patch

import pandas as pd
import pytest


@pytest.fixture()
def test_files():
    """Return the directory with the files for testing."""

    return Path.cwd().joinpath("tests", "test_files")


@pytest.fixture()
def pandas_arguments_download():
    """Return a dict with the keyword arguments for pandas."""

    return {
        "csv": {"delimiter": ",", "index_col": 0},
        "json": {"orient": "index"},
        "txt": {"delimiter": ",", "index_col": 0},
        "xls": {"index_col": 0},
        "xlsx": {"index_col": 0},
        "parquet": {},
    }


@pytest.fixture()
def pandas_arguments_upload():
    """Return a dict with the keyword arguments for pandas."""

    return {
        "csv": {"header": ["one", "two"]},
        "json": {"orient": "index"},
        "txt": {"header": ["one", "two"]},
        "xls": {"header": ["one", "two"]},
        "xlsx": {"header": ["one", "two"]},
        "parquet": {},
    }


@pytest.fixture()
def dataframe_upload():
    """Return a dict with the keyword arguments for pandas."""

    def _make_dataframe(file_extension, file, additional_kwargs=None, stream=False):
        """Make a pandas DataFrame."""

        if not additional_kwargs:
            additional_kwargs = {}

        if file_extension in [".csv", ".txt"]:
            arguments = {"index_col": 0, "delimiter": ",", "float_precision": "high"}
            arguments.update({key: value for key, value in additional_kwargs.items()})
            if not stream:
                return pd.read_table(file, **arguments)
            return pd.read_table(io.StringIO(file), **arguments)
        elif file_extension in [".xls", ".xlsx"]:
            if file_extension == ".xls" and not stream:
                return pd.read_excel(
                    file, index_col=0, engine="xlrd", **additional_kwargs
                )
            return pd.read_excel(
                file, index_col=0, engine="openpyxl", **additional_kwargs
            )
        elif file_extension == ".json":
            return pd.read_json(file, **additional_kwargs)
        elif file_extension == ".parquet":
            # with open(file) as f:
            #     file = pd.read_parquet(f, engine="pyarrow", **additional_kwargs)
            # # test = io.BytesIO()
            # assert file == Path('/home/uijl/checkout/pandablob/tests/test_files/test_data.parquet')
            return pd.read_parquet(file, engine="pyarrow", **additional_kwargs)

    return _make_dataframe


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
