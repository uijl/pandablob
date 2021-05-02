![PyTest](https://github.com/uijl/pandablob/workflows/PyTest/badge.svg)
[![PyPI Latest Release](https://img.shields.io/pypi/v/pandablob.svg)](https://pypi.org/project/pandablob/)
[![Downloads](https://pepy.tech/badge/pandablob)](https://pepy.tech/project/pandablob)

# PandaBlob

Functions to easily transform Azure blobs into pandas DataFrames and vice versa. 

## Installation

Installing PandaBlob via [pip](https://pip.pypa.io) is the preferred method, as it will always install the most recent stable release. If you do not have
[pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

To install PandaBlob, run this command in your terminal:

```bash
# Use pip to install PandaBlob
pip install pandablob
```

Downloading and installing PandaBlob from source is also possible, follow the code below.

```bash
# Download the package
git clone https://github.com/uijl/pandablob

# Go to the correct folder
cd pandablob

# Install package
pip install -e .
```

## Usage

The code snip below shows how you can use PandaBlob, all you need is a _[BlobClient](https://docs.microsoft.com/nl-nl/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python)_ and possibly a pandas DataFrame or some keyword arguments for pandas.

```python
# Import the Azure SDK and pandablob
import pandablob

from azure.storage.blob import ContainerClient

# Your Azure Credentials
account_url = "https://my_account_url.blob.core.windows.net/"
token = "your_key_string"
container = "your_container"
blobname = "your_blob_name.csv"

container_client = ContainerClient(account_url, container, credential=token)
blob_client = container_client.get_blob_client(blob=blobname)

# Specifiy your pandas keyword arguments
pandas_kwargs = {"index_col": 0}

# Read the blob as a pandas DataFrame
df = pandablob.blob_to_df(blob_client, pandas_kwargs)
```

## Potential errors

There are three common errors that can be returned. Two are related to the blob storage and one because of the current limitations of pandablob.

- **ResourceExistsError** - If the specified blob is already on the blob, this error is returned. There are two options, you can add the `overwrite=True` argument to your `df_to_blob` function or you can catch the exception. If you wish to enter it in an except statement, you can import it using `from azure.core.exceptions import ResourceExistsError`;
- **ResourceNotFoundError** - If the specified blob is not found, this error is returned. If you wish to enter it in an except statement, you can import it using `from azure.core.exceptions import ResourceNotFoundError`;
- **TypeError** - This error is returned by pandablob if you want to upload or download an extensiontype that is not yet supported. Currently only the following extensions are supported: `.csv` `.json` `.txt`, `.xls` and `.xlsx`.

## To do list:

Some other stuff that needs to be done:

- [ ] Include other files;
- [x] Easier downloading a .csv file;
- [x] Added MIT license.
