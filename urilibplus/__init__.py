"""
urilibplus

A python module containing classes used to interact and manipulate
uris in python in a easier and consistent manner.
"""

#pylint:disable=invalid-name

from .uri_path import URIPath
from .uri_query import URIQuery
from .uri import URI
from .characters import CharacterSets

__version__ = "1.0.0.0"
__all__ = ["URI", "URIPath", "URIQuery", "CharacterSets"]
