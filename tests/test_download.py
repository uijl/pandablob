"""Test downloading a blob and returning a DataFrame."""

import io

import pandas as pd
import pytest

import pandablob


@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx", "parquet"])
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
    if extension == ".csv":
        compare_df = pd.read_csv(file_location)
        assert df.equals(compare_df)
    if extension == ".txt":
        compare_df = pd.read_table(file_location)
        assert df.equals(compare_df)
    if extension == ".json":
        compare_df = pd.read_json(file_location)
        assert df.equals(compare_df)
    if extension == ".xls":
        compare_df = pd.read_excel(file_location, engine="xlrd")
        assert df.equals(compare_df)
    if extension == ".xlsx":
        compare_df = pd.read_excel(file_location, engine="openpyxl")
        assert df.equals(compare_df)
    if extension == ".parquet":
        compare_df = pd.read_parquet(file_location, engine="pyarrow")
        assert df.equals(compare_df)
