"""Test downloading a blob and returning a DataFrame with given kwargs."""

import io

import pandas as pd
import pytest

import pandablob


@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx", "parquet"])
def test_download_kwargs(mock_download, test_files, pandas_arguments_download, file):
    """Mock downloading from the azure blob with additional kwargs."""

    # Create required input
    file_name = f"test_data.{file}"
    file_location = test_files.joinpath(file_name)
    extension = file_location.suffix

    # Get mock object from fixture
    MockAzureBlob = mock_download(file_name, file_location)

    # Download blob and make DataFrame
    df = pandablob.blob_to_df(MockAzureBlob, pandas_arguments_download[file])

    # download blob and return DataFrame
    if extension == ".csv" or extension == ".txt":
        compare_df = pd.read_table(file_location, delimiter=",", index_col=0)
        assert df.equals(compare_df)
    elif extension == ".json":
        compare_df = pd.read_json(file_location, orient="index")
        assert df.equals(compare_df)
    elif extension == ".xls":
        compare_df = pd.read_excel(file_location, index_col=0, engine="xlrd")
        assert df.equals(compare_df)
    elif extension == ".xlsx":
        compare_df = pd.read_excel(file_location, index_col=0, engine="openpyxl")
        assert df.equals(compare_df)
    elif extension == ".parquet":
        compare_df = pd.read_parquet(file_location, engine="pyarrow")
        assert df.equals(compare_df)
