"""Test uploading a DataFrame to a specified a blob with given kwargs."""

import io

import pandas as pd
import pytest

import pandablob


@pytest.mark.parametrize("file", ["csv", "json", "txt", "xls", "xlsx", "parquet"])
def test_upload_kwargs(
    file, test_files, dataframe_upload, pandas_arguments_upload, mock_upload
):
    """Mock uploading with additional kwargs to the azure blob."""

    # Create required input
    file_name = f"test_data.{file}"
    file_location = test_files.joinpath(file_name)
    extension = file_location.suffix

    # Get mock object from fixture
    MockAzureBlob = mock_upload(file_name)

    # Make DataFrame to upload
    df = dataframe_upload(extension, file_location)
    pandablob.df_to_blob(df, MockAzureBlob, pandas_arguments_upload[file])

    # Mock uploading the DataFrame
    pandablob_stream = MockAzureBlob.upload_blob.call_args[0][0]

    # Test result
    if extension == ".json":
        result_df = dataframe_upload(
            extension, pandablob_stream, pandas_arguments_upload[file], True
        )
    else:
        result_df = dataframe_upload(extension, pandablob_stream, stream=True)
        df.columns = ["one", "two"]

    assert df.equals(result_df)
