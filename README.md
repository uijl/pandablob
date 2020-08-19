[![CircleCI Status](https://circleci.com/gh/uijl/wtdpy.svg?style=svg)](https://circleci.com/gh/uijl/wtdpy)
[![Documentation Status](https://readthedocs.org/projects/wtdpy/badge/?version=latest)](https://wtdpy.readthedocs.io/en/latest/?badge=latest)
[![Coverage Badge](https://artifact-getter.herokuapp.com/get_coverage_badge?circle_url=https://circleci.com/gh/uijl/wtdpy&circle_token=4&output=str)](https://artifact-getter.herokuapp.com/get_coverage_report?circle_url=https://circleci.com/gh/uijl/wtdpy&circle_token=4)
[![PyPI Latest Release](https://img.shields.io/pypi/v/wtdpy.svg)](https://pypi.org/project/wtdpy/)

# WTDpy

Basic calls to the World Trading Data API with Python. 
You can find the documentation over [here](https://wtdpy.readthedocs.io).

## Installation

Installing WTDpy via [pip](https://pip.pypa.io) is the preferred method, as it will always install the most recent stable release. If you do not have
[pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

To install WTDpy, run this command in your terminal:

``` bash
# Use pip to install wtdpy
pip install wtdpy
```

Downloading and installing WTDpy from source is also possible, follow the code below.

``` bash
# Download the package
git clone https://github.com/uijl/wtdpy

# Go to the correct folder
cd wtdpy

# Install package
pip install -e .
```

## Starting up

The code snip below shows how you can initialise the WTDpy class. As soon as you have the `WTDpy` class initialised you can start calling the various functions.

```python
# Import wtdpy library
from wtdpy import WTDpy

# Specifiy your api key
api_token = "Your_API_Token"

# Initialise class
wtdpy = WTDpy(api_token=api_token)

# Search for a stock or index
MSFT = wtdpy.search("Microsoft")
```
