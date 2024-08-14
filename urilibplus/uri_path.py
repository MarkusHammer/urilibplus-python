""" 
`uri_path`

Holds the `URIPath` class and reated imports.
"""

from urllib.parse import quote as uriquote

from sys import maxsize as sys_maxsize, version_info
from re import compile as regexcompile

from .characters import CharacterSets
from .tools import iter_flatten
from .typings import * # pylint: disable=wildcard-import, unused-wildcard-import

class URIPath(PurePosixPath, PathLike, MutableSequenceABC[str]):
    """
    `URIPath`

    A class used to manipulate and use a URI path in python easily.
    """

    _USE_NEW_PUREPATH_INIT_METHOD:bool = version_info.major > 3 or (version_info.major == 3 and
                                                                    version_info.minor >= 12)
    _CACHEING_ANCESTORS:Tuple[type, ...] = (PurePosixPath, PurePath, PureWindowsPath)
    _CACHE_ATTR_NAMES:Iterator[LiteralString] = cast(Iterator[LiteralString],
                                                     iter_flatten(
                                                         (getattr(c, "__slots__", []) for c in _CACHEING_ANCESTORS), #pylint:disable=line-too-long
                                                         str
                                                         )
                                                     )
    @property
    def raw(self) -> List[str]:
        """
        `__raw`

        Used internally, do not modify without express intent.

        Returns:
            The internal list of strings used by `Path` types to create paths from.
        """
        return self._raw_paths
    @raw.setter
    def raw(self, value:List[str]):
        #without this, the caches parts of the path wont update when we manually change the content
        for attr in self._CACHE_ATTR_NAMES:
            if hasattr(self, attr):
                delattr(self, attr)
        self._raw_paths = value
    @raw.deleter
    def raw(self):
        # you don't just delete raw, but you can clear it...
        self.raw = []

    def __new__(cls,
                *path:Union[str, PathLike, Iterable[Union[str, PathLike]]],
                unquote: bool = False,
                requote:bool = False,
                quote_safe:str = ""
               ) -> 'URIPath':
        # don't run the inherited __new__ methods,
        # it automatically makes the path in the OS local type and confuses type checkers
        if cls._USE_NEW_PUREPATH_INIT_METHOD or TYPE_CHECKING:
            return object.__new__(cls)
        else:
            return cls._from_parts(tuple(iter_flatten(path, str)))

    def __init__(self,
                 *path:Union[str, PathLike, Iterable[Union[str, PathLike]]],
                 unquote:bool = False,
                 requote:bool = False,
                 quote_safe:str = ""
                ):
        self.unquote:bool = unquote
        self.requote:bool = requote
        self.quote_safe = quote_safe

        if self._USE_NEW_PUREPATH_INIT_METHOD:
            super().__init__(*tuple(iter_flatten(path, str)))

    def __iter__(self):
        return iter(self.parts)

    @overload
    def __getitem__(self, index:int) -> str: ...
    @overload
    def __getitem__(self, index:slice) -> List[str]: ...
    def __getitem__(self, index:Union[int, slice]) -> Union[str, List[str]]:
        return list(self.parts[index])

    def __setitem__(self,
                    index:Union[int, slice],
                    value:Union[str, PathLike, Iterable[Union[str, PathLike]]]
                   ):
        c = list(self)

        value = self.copy(value)

        if isinstance(index, int):
            c[index] = str(value)
        else:
            c[index] = list(value)

        self.raw = c

    def __delitem__(self, index:Union[int, slice]):
        c = list(self)
        del c[index]
        self.raw = c

    def __bool__(self):
        return not self.isempty()

    def __len__(self):
        return len(self.parts)

    def __truediv__(self, other:Union[str, PathLike, Iterable[Union[str, PathLike]]]): #self / other
        c = self.copy()
        c.append(other)
        return c

    @overload
    def __contains__(self,                                                     #type:ignore
                     other:Union[str, PathLike, Iterable[Union[str, PathLike]]]
                    ) -> bool: ...
    @overload
    def __contains__(self, other:object) -> NotImplementedType: ...
    def __contains__(self,
                     other:Union[str, PathLike, Iterable[Union[str, PathLike]], object]
                    ) -> Union[bool, NotImplementedType]:
        if not isinstance(other, (str, PathLike, Iterable)):
            return NotImplemented
        return all((x in list(self)) for x in self.copy(other))

    def copy(self,
             *content_override:Union[str, PathLike, Iterable[Union[str, PathLike]]]
            ) -> 'URIPath':
        """
        `copy`

        `*content_override` -- When any of these arguments are set,
            the copy will instead be initialised with these values as the path's content.

        Returns:
            A complete, deep, copy of this object; with the contents optionally overridden.
        """
        kwargs = {
            "unquote":self.unquote,
            "requote":self.requote,
            "quote_safe":self.quote_safe
        }

        return URIPath(*((self,) if len(content_override) <= 0 else content_override), **kwargs)
    __copy__ = copy
    __deepcopy__ = copy

    def append(self, value:Union[str, PathLike, Iterable[Union[str, PathLike]]]):
        appendage = []
        if isinstance(value, URIPath) :
            if all(not x.startswith("/") for x in value.raw):
                appendage = value.raw
            else:
                appendage = list(value[1:] if value[0] == "/" else value[:])
        else:
            appendage = self.copy(value).raw
        self.raw = self.raw + appendage

    def count(self, value:str) -> int:
        return list(self).count(value)

    def index(self, value:str, start:int = 0, stop:int = sys_maxsize) -> int:
        return list(self).index(value, start, stop)

    def rindex(self, value:str, start:int = 0, stop:Optional[int] = None) -> int:
        """
        `rindex`

        Similar to `index`, but searching in reverse order.

        Arguments:
            value -- The value to search for.

        Keyword Arguments:
            start -- The lower index to limit searches at, defaults to 0.
            stop -- The higher index to limit searches at, defaults to `None`,
                which equates to stopping at the end of the list.

        Returns:
            The index found.
        """
        return (len(self) - self[start:stop][-1::-1].index(value) - 1) + abs(start)

    def insert(self, index:int, value:Union[str, PathLike, Iterable[Union[str, PathLike]]]):
        value = self.copy(value).raw
        self.raw = self.raw[:index] + value + self.raw[index:]

    def remove(self, value:str):
        newraw = list(self.copy(value))
        newraw.remove(value)
        self.raw = newraw

    def isempty(self) -> bool:
        """
        `isempty`

        Returns:
            `True` if the path contains no segments, otherwise `False`.
        """
        return len(self.raw) <= 0

    def encode(self, quote: Optional[bool] = None, quote_safe:Optional[str] = None) -> str:
        """
        `encode`

        Keyword Arguments:
            quoted -- If not `None`, the path will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            The path object, encoded as a string.
        """
        if quote is None:
            quote = self.requote

        if quote_safe is None:
            quote_safe = cast(str, self.quote_safe)

        quote_safe += "/"

        if not quote:
            return super().__str__()
        else:
            seg = tuple(uriquote(x, quote_safe) for x in self)
            if self[0] == "/": #the root slash will be consitered a part, we need to preserve that
                seg = ("/", ) + seg[1:]
            return super(URIPath, self.copy(*seg)).__str__()
    __str__ = encode
    __repr__ = encode

    def validate(self, encoded:bool = False) -> bool:
        """
        `validate`

        Returns:
            True if all characters in this object are allowed in a URI's path.
        """
        if encoded:
            return not CharacterSets.invalid_check(CharacterSets.PATH, self.encode(True))
        else:
            return not CharacterSets.invalid_check(CharacterSets.SEGMENT, *tuple(self))

    def segafter(self, value: str, last:bool = False) -> Union[str, None]:
        """
        `segafter`
        
        Retrieves the content of the after the first (or last)
        path segment matching `value`, if any; otherwise None.

        Arguments:
            value -- The exact value of a segment to find.

        Keyword Arguments:
            last -- Instead of finding the first possible segment matching `value`,
                find the last.

        Returns:
            The content of the segment comming after the found `value`,
            or `None` if `value` was not found.
        """
        if value not in self:
            return None

        ind = (self.rindex if last else self.index)(value)
        if ind >= len(self):
            return None

        return cast(str, self[ind + 1])

    def segbefore(self, value: str, last:bool = False) -> Union[str, None]:
        """
        `segbefore`
        
        Retrieves the content of the before the first (or last)
        path segment matching `value`, if any; otherwise None.

        Arguments:
            value -- The exact value of a segment to find.

        Keyword Arguments:
            last -- Instead of finding the first possible segment matching `value`,
                find the last.

        Returns:
            The content of the segment comming before the found `value`,
            or `None` if `value` was not found.
        """
        if value not in self:
            return None

        ind = (self.rindex if last else self.index)(value)
        if ind <= 0:
            return None

        return cast(str, self[ ind - 1])

    def segsearch(self,
                  pattern:Union[str, Pattern],
                  include_all:bool = False
                 ) -> Iterable[Match]:
        """
        `segsearch`

        Searches every segment in the path for the given regex `pattern`,
        returning any found as an iterable.

        Arguments:
            `pattern` -- The pattern to search for in each segment.

        Keyword Arguments:
            `include_all` -- Return every match found in a single segment, not just the first one.

        Returns:
            A iterable of found matches, in the same rough
            order of the segment they where found in.

        Yields:
            A match found.
        """
        if isinstance(pattern, str):
            pattern = regexcompile(pattern)

        for s in self:
            m = pattern.search(s)
            if include_all or m is not None:
                yield cast(Match, m)
