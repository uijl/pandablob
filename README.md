![PyTest](https://github.com/uijl/pandablob/workflows/PyTest/badge.svg)
[![PyPI Latest Release](https://img.shields.io/pypi/v/pandablob.svg)](https://pypi.org/project/pandablob/)

# PandaBlob

Functions to easily transform Azure blobs into pandas DataFrames and vice versa. 

## Installation

Installing PandaBlob via [pip](https://pip.pypa.io) is the preferred method, as it will always install the most recent stable release. If you do not have
[pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

To install PandaBlob, run this command in your terminal:

``` bash
# Use pip to install PandaBlob
pip install pandablob
```

Downloading and installing PandaBlob from source is also possible, follow the code below.

``` bash
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
pandas_kwargs = {"delimiter": ",", "index_col": 0}

# Read the blob as a pandas DataFrame
df = pandablob.blob_to_df(blob_client, pandas_kwargs)
```

## To do list:

Some other stuff that needs to be done:

- [ ] Include other files;
- [ ] Easier downloading a .csv file;
