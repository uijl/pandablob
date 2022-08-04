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
        elif extension == ".json":
            df.to_json(string_io, **pandas_kwargs)
        return blob_client.upload_blob(string_io.getvalue(), overwrite=overwrite)
    elif extension in [".xls", ".xlsx", ".parquet"]:
        bytes_io = io.BytesIO()
        if extension in [".xls", ".xlsx"]:
            df.to_excel(bytes_io, **pandas_kwargs)
        elif extension == ".parquet":
            df.to_parquet(bytes_io, **pandas_kwargs)
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
    data_stream = io.BytesIO(blob_client.download_blob().readall())
    if extension == ".csv":
        return pd.read_csv(data_stream, **pandas_kwargs)
    elif extension == ".txt":
        return pd.read_table(data_stream, **pandas_kwargs)
    elif extension == ".json":
        return pd.read_json(data_stream, **pandas_kwargs)
    elif extension == ".parquet":
        return pd.read_parquet(data_stream, **pandas_kwargs)
    elif extension in [".xls", ".xlsx"]:
        if extension == ".xls" and "engine" not in pandas_kwargs.keys():
            pandas_kwargs.update({"engine": "xlrd"})
        elif "engine" not in pandas_kwargs.keys():
            pandas_kwargs.update({"engine": "openpyxl"})
        return pd.read_excel(data_stream, **pandas_kwargs)

    raise TypeError(f"{extension} files are not yet supported.")
