# colivara-py

[![PyPI](https://img.shields.io/pypi/v/colivara-py.svg)](https://pypi.org/project/colivara-py/)
[![Tests](https://github.com/tjmlabs/colivara-py/actions/workflows/test.yml/badge.svg)](https://github.com/tjmlabs/colivara-py/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/tjmlabs/colivara-py?include_prereleases&label=changelog)](https://github.com/tjmlabs/colivara-py/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/tjmlabs/colivara-py/blob/main/LICENSE)

The official Python SDK for the ColiVara API

## Installation

Install this library using `pip`:
```bash
pip install colivara-py
```
## Usage

Usage instructions go here.

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

We use uv, but you can use the pip interface if you prefer:

```bash
cd colivara-py
uv .venv
source .venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
uv sync --extra dev-dependencies
```
To run the tests:
```bash
pytest
```
