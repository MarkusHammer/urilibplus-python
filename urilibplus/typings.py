""" 
`typings`

Holds the imported types used for type checking and inheriting
"""

# pylint:disable=unused-import, ungrouped-imports, deprecated-class

from re import Pattern, Match

from os import PathLike

from collections import UserList

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

try:
    from typing import TypeVar
except ImportError:
    from typing_extensions import TypeVar

try:
    from pathlib import PurePosixPath
except ImportError:
    from pathlib2 import PurePosixPath #type:ignore

try:
    from pathlib import PurePath
except ImportError:
    from pathlib2 import PurePath #type:ignore

try:
    from pathlib import PureWindowsPath
except ImportError:
    from pathlib2 import PureWindowsPath #type:ignore

try:
    from typing import Iterable
except ImportError:
    from typing_extensions import Iterable

try:
    from typing import Iterator
except ImportError:
    from typing_extensions import Iterator

try:
    from typing import List
except ImportError:
    from typing_extensions import List

try:
    from typing import Tuple
except ImportError:
    from typing_extensions import Tuple

try:
    from typing import Union
except ImportError:
    from typing_extensions import Union

try:
    from typing import Optional
except ImportError:
    from typing_extensions import Optional

try:
    from typing import Dict
except ImportError:
    from typing_extensions import Dict

try:
    from typing import NoReturn
except ImportError:
    from typing_extensions import NoReturn

try:
    from typing import Any
except ImportError:
    from typing_extensions import Any

try:
    from typing import SupportsIndex
except ImportError:
    from typing_extensions import SupportsIndex

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

try:
    from typing import Sequence
except ImportError:
    from typing_extensions import Sequence

try:
    from typing import LiteralString #type:ignore #this isn't declaired if it fails
except ImportError:
    from typing_extensions import LiteralString #type:ignore #this isn't declaired if it fails

try:
    from typing import cast
except ImportError:
    from typing_extensions import cast

try:
    from typing import overload
except ImportError:
    from typing_extensions import overload

try:
    from typing import Sized
except ImportError:
    from typing_extensions import Sized

try:
    from typing import MutableSequence
except ImportError:
    from typing_extensions import MutableSequence

from collections.abc import MutableSequence as MutableSequenceABC

try:
    from types import NotImplementedType #type:ignore
except ImportError:
    NotImplementedType:TypeAlias = Any

try:
    from typing import TYPE_CHECKING
except ImportError:
    try:
        from typing_extensions import TYPE_CHECKING
    except ImportError:
        TYPE_CHECKING:bool = False
