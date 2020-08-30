"""Test uploading a DataFrame to a specified a blob."""

import io

import pandas as pd
import pytest

import pandablob


@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx"])
def test_upload(file, test_files, pandas_arguments, mock_upload):
    """Mock uploading to the azure blob."""

    # Create required input
    file_name = f"test_data.{file}"
    file_location = test_files.joinpath(file_name)
    extension = file_location.suffix

    # Get mock object from fixture
    MockAzureBlob = mock_upload(file_name)

    # Make DataFrame to upload
    if extension == ".csv" or extension == ".txt":
        df = pd.read_table(file_location, delimiter=",")
        pandablob.df_to_blob(df, MockAzureBlob)
    elif extension == ".json":
        df = pd.read_json(file_location)
        pandablob.df_to_blob(df, MockAzureBlob)
    elif extension == ".xlsx" or extension == ".xls":
        df = pd.read_excel(file_location)
        pandablob.df_to_blob(df, MockAzureBlob)

    # Mock uploading the DataFrame
    pandablob_stream = MockAzureBlob.upload_blob.call_args[0][0]
    if extension == ".csv":
        result_df = pd.read_table(
            io.StringIO(pandablob_stream.get_value()),
            index_col=0,
            delimiter=",",
            float_precision="high",
        )
    elif extension == ".txt":
        result_df = pd.read_table(
            io.StringIO(pandablob_stream.get_value()),
            index_col=0,
            delimiter=",",
            float_precision="high",
        )
    elif extension == ".json":
        result_df = pd.read_json(pandablob_stream)
    elif extension == ".xlsx" or extension == ".xls":
        result_df = pd.read_excel(pandablob_stream)

    # Test result
    # assert df.equals(result_df)

    for ix in df.index:
        for col in df.columns:
            assert df.loc[ix, col] == result_df.loc[ix, col]
