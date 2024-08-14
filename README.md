
# `urilibplus`

> A Python Module for URI Manipulation. Inspired by `pathlib`, but for URIs.

`urilibplus` is a Python module designed to simplify the interaction and manipulation of URIs. It provides the `URI` class, which encapsulates URI operations into a consistent and user-friendly interface.
With this module, you can easily handle URIs, including tasks such as encoding, validation, and manipulation.

[Documentation](https://MarkusHammer.gthub.io/urilibplus-python)

## Setup

This module can be installed using:

```bash
pip install urilibplus
```

## Usage

This module is intended to be used only as a module, and can be imported after installing using the traditional process:

```python
from urilibplus import URI
```

### Creating a URI Object

```python
uri = URI("http://user:pass@host:1234/path?query#fragment")
print(uri.scheme)  # outputs "http"
print(uri.authority)  # outputs "user:pass@host:1234"
```

### Encoding and Decoding URIs

```python
encoded_uri = uri.encode() #same as str(uri)
print(encoded_uri) # outputs "http://user:pass@host:1234/path?query#fragment"

decoded_uri = URI(encoded_uri)
print(decoded_uri) # outputs "http://user:pass@host:port/path?query#fragment"

print(uri.encode(quote = True)) #outputs "http%3A%2F%2Fuser%3Apass%40host%3A1234%2Fpath%3Fquery%23fragment"
```

### Path Manipulation

Also see the [docs](https://MarkusHammer.gthub.io/urilibplus-python) for the `URIPath` object, an object for `URI`s that works exactly like a `pathlib` path.
Every `URI` object makes use of a `URIPath` object.

```python
uri.pathappend("subpath", "suberpath")
print(uri.encode())  # outputs "http://user:pass@host:1234/path/subpath/suberpath?query#fragment"
```

### And More

There are a handfull of other ease of use features that this module provides, feel free to reference the [documentation](https://MarkusHammer.gthub.io/urilibplus-python) for more information.

## Licence

This is licensed under the Mozilla Public License 2.0 (MPL 2.0) Licence. See the Licence file in this repository for more information.

## Contribute

Contributions are always welcome!
Use the [github repository](https://github.com/MarkusHammer/urilibplus-python) to report issues and contribute to this project.

## Credits

While not required, feel free to credit "Markus Hammer" (or just "Markus") if you find this code or script useful for whatever you may be doing with it.
