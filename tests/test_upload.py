"""Test uploading a DataFrame to a specified a blob."""

import io

import pandas as pd
import pytest

import pandablob


@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx", "parquet"])
def test_upload(file, test_files, dataframe_upload, mock_upload):
    """Mock uploading to the azure blob."""

    # Create required input
    file_name = f"test_data.{file}"
    file_location = test_files.joinpath(file_name)
    extension = file_location.suffix

    # Get mock object from fixture
    MockAzureBlob = mock_upload(file_name)

    # Make DataFrame to upload
    df = dataframe_upload(extension, file_location)
    pandablob.df_to_blob(df, MockAzureBlob)

    # Mock uploading the DataFrame
    pandablob_stream = MockAzureBlob.upload_blob.call_args[0][0]

    # Test result
    if extension == ".parquet":
        pandablob_stream = io.BytesIO(pandablob_stream)
    result_df = dataframe_upload(extension, pandablob_stream, stream=True)

    if extension == ".parquet":
        result_df.set_index("Unnamed: 0", drop=True, inplace=True)
        df.set_index("Unnamed: 0", drop=True, inplace=True)

    assert df.equals(result_df)
