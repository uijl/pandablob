"""Test downloading a blob and returning a DataFrame."""

import io

import pandas as pd
import pytest

import pandablob


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx"])
def test_download(file, test_files, mock_download):
    """Mock uploading to the azure blob."""

    # Create required input
    file_name = f"test_data.{file}"
    file_location = test_files.joinpath(file_name)
    extension = file_location.suffix

    # Get mock object from fixture
    MockAzureBlob = mock_download(file_name, file_location)

    # Download blob and make DataFrame
    df = pandablob.blob_to_df(MockAzureBlob)

    # Make DataFrame from original file and compare
    if extension == ".csv" or extension == ".txt":
        compare_df = pd.read_table(file_location)
        assert df.equals(compare_df)
    if extension == ".json":
        compare_df = pd.read_json(file_location)
        assert df.equals(compare_df)
    if extension == ".xlsx" or extension == ".xls":
        compare_df = pd.read_excel(file_location)
        assert df.equals(compare_df)
