import io
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
from azure.storage.blob import BlobClient


def df_to_blob(
    df: pd.DataFrame,
    blob_client: BlobClient,
    pandas_kwargs: Optional[Dict[str, Any]] = None,
    overwrite: bool = False,
) -> None:
    """Upload a pandas DataFrame and store it into a blob."""

    # check for kwargs
    if not pandas_kwargs:
        pandas_kwargs = {}

    # check the file extension
    extension = Path(blob_client.blob_name).suffix

    # make DataFrame and upload
    if extension in [".csv", ".txt", ".json"]:
        string_io = io.StringIO()
        if extension in [".csv", ".txt"]:
            df.to_csv(string_io, **pandas_kwargs)
        if extension == ".json":
            df.to_json(string_io, **pandas_kwargs)
        return blob_client.upload_blob(string_io.getvalue(), overwrite=overwrite)
    if extension in [".xls", ".xlsx"]:
        bytes_io = io.BytesIO()
        if extension == ".xls":
            pandas_kwargs.update({"engine": "xlrd"})
        else:
            pandas_kwargs.update({"engine": "openpyxl"})
        df.to_excel(bytes_io, **pandas_kwargs)
        return blob_client.upload_blob(bytes_io.getvalue(), overwrite=overwrite)

    raise TypeError(f"{extension} files are not yet supported.")


def blob_to_df(
    blob_client: BlobClient, pandas_kwargs: Optional[Dict[str, Any]] = None
) -> pd.DataFrame:
    """Download a blob and return a pandas DataFrame."""

    # check for kwargs
    if not pandas_kwargs:
        pandas_kwargs = {}

    # check the file extension
    extension = Path(blob_client.blob_name).suffix

    # download blob and return DataFrame
    if extension == ".csv" or extension == ".txt":
        data_stream = io.BytesIO(blob_client.download_blob().readall())
        return pd.read_table(data_stream, **pandas_kwargs)
    if extension == ".json":
        data_stream = io.BytesIO(blob_client.download_blob().readall())
        return pd.read_json(data_stream, **pandas_kwargs)
    if extension == ".xlsx" or extension == ".xls":
        data_stream = io.BytesIO(blob_client.download_blob().readall())
        return pd.read_excel(data_stream, **pandas_kwargs)

    raise TypeError(f"{extension} files are not yet supported.")
