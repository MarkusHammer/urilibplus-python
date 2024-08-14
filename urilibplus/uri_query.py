""" 
`uri_query`

Holds the `URIQuery` class and reated imports.
"""

from urllib.parse import (parse_qsl as uriqueryparse,
                          urlencode as uriqueryunparse,
                          quote as uriquote,
                          unquote as uriunquote)
from sys import maxsize as sys_maxsize
from re import compile as regexcompile

from .characters import CharacterSets
from .typings import * # pylint: disable=wildcard-import, unused-wildcard-import
from .tools import passthrough_first

class URIQuery(UserList):
    """
    `URIQuery`

    A class used to manipulate and use a URI query in python easily.
    
    NOTE: while this class acts and appears very similar to a tuple of dictionary items,
    it is not, as it allows for duplacate keys, and requires the ordering to be preserved.
    """

    def __parse(self, querystr:str) -> List[Tuple[str, str]]:
        parsed = uriqueryparse(querystr, keep_blank_values=True, strict_parsing = True)
        return parsed if not self.unquote else [(uriunquote(k), uriunquote(v)) for k,v in parsed]

    def __init__(self,
                 content:Union[str, List[Tuple[str, str]], Dict[str, str], 'URIQuery', None]= None,
                 *,
                 unquote:bool = False, #unquote values when unencoding strings
                 requote: bool = False, #requote values when normalizing to string
                 force_case: Literal["upper", "lower", "preserve"] = "preserve",
                 quote_safe: str = ""
                ):
        self.unquote:bool = unquote
        self.requote:bool = requote
        self.quote_safe:str = quote_safe
        self.force_case: Literal["upper", "lower", "preserve"] = force_case
        self.data:List[Tuple[str, str]]

        if isinstance(content, (dict, URIQuery)):
            content = list(content.items())
        elif isinstance(content, str):
            content = content.strip().lstrip("?").lstrip()
            if content == "":
                content = None
            else:
                if "=" not in content:
                    #normaize a nonstandard query with a empty value while still in string form
                    content += "="
                content = self.__parse(content)

        super().__init__(content)

    def __bool__(self):
        return not self.isempty()

    def __lshift__(self, count:int) -> 'URIQuery':
        c = self.copy()
        if count > 0:
            for _ in range(count):
                c.append(c.pop(0))
        else:
            for _ in range(abs(count)):
                c.insert(0, c.pop(-1))
        return c

    def __rshift__(self, count:int) -> 'URIQuery':
        return self << -count

    def __add__(self,
                other:Union[str, Tuple[str, str], Iterable[Tuple[str, str]], 'URIQuery']
               ) -> 'URIQuery':
        c = self.copy()

        if isinstance(other, str):
            other = self.__parse(other)
        elif isinstance(other, URIQuery):
            other = other.data
        elif (isinstance(other, tuple) and
              len(other) == 2 and
              isinstance(other[0], str) and
              isinstance(other[1], str)
             ):
            other = [cast(Tuple[str, str], other)]
        else:
            other = list(cast(Iterable[Tuple[str, str]], other))

        c.data += other

        return c

    def __len__(self):
        return len(self.data)

    def append(self, item:Union[str, Tuple[str, str], Iterable[Tuple[str, str]]]):
        #we can use the __add__ opperator, as this appcompishes the same thing
        self.data = list(self + item)

    def count(self, item:Union[str, Tuple[str, str]]) -> int:
        if isinstance(item, str):
            parsed = self.__parse(item)
            if len(parsed) == 1:
                item = parsed[0]
            else:
                raise TypeError(item)

        return super().count(item)

    def index(self,                                        #pylint:disable=arguments-differ
              item:Union[str, Tuple[str, str]],
              start:Union[int, SupportsIndex] = 0,
              stop:Union[int, SupportsIndex] = sys_maxsize
             ) -> int:
        if isinstance(item, str):
            parsed = self.__parse(item)
            if len(parsed) == 1:
                item = parsed[0]
            else:
                raise TypeError(item)

        return super().index(item, start, stop)

    def insert(self, i:int, item:Union[str, Tuple[str, str]]):
        if isinstance(item, str):
            parsed = self.__parse(item)
            if len(parsed) == 1:
                item = parsed[0]
            else:
                raise TypeError(item)

        super().insert(i, item)

    def remove(self, item:Union[str, Tuple[str, str]]):
        if isinstance(item, str):
            parsed = self.__parse(item)
            if len(parsed) == 1:
                item = parsed[0]
            else:
                raise TypeError(item)

        super().remove(item)

    def querykeys(self, *values:str) -> Iterable[str]:
        """
        `querykeys`

        Returns:
            An iterable with all keys of this query,
            or only the keys with one of the exact `*values` given,
            if any `*values` are given.
        """
        return (k for k,v in self if len(values) <= 0 or v in values)

    def queryvalues(self, *keys:str) -> Iterable[str]:
        """
        `queryvalues`

        Returns:
            An iterable with all values of this query,
            or only the values with one of the exact `*keys` given,
            if any `*keys` are given.
        """
        return (v for k,v in self if len(keys) <= 0 or k in keys)

    def items(self, *kvpairs:Tuple[str,str]) -> Iterable[Tuple[str, str]]:
        """
        `items`

        Returns:
            An iterable with all items of this query (formated as a tuple of `("key", "value")`),
            or only the values with one of the exact `*kvpairs` given,
            if any `*kvpairs` are given.
        """
        return (self.data if len(kvpairs) <= 0 else((k,v) for k,v in self if (k,v) in kvpairs))

    def keyindexes(self, *keys:str) -> Tuple[int, ...]:
        """
        `keyindexes`

        Returns:
            An iterable with all indexes of all entries with one of the exact `*keys` in this query.
        """
        return tuple(i for i,(k,v) in enumerate(self) if k in keys)

    def valueindexes(self, *values:str) -> Tuple[int, ...]:
        """
        `valueindexes`

        Returns:
            An iterable with all indexes of all entries
            with one of the exact `*value` in this query.
        """
        return tuple(i for i,(k,v) in enumerate(self) if v in values)

    #dictionary like methods
    def getvalues(self, key:str) -> Tuple[str, ...]:
        """
        `getvalues`

        A dictionary like get method.

        Returns:
            A tuple with all values found with the given `key`.
        """
        return tuple(self.queryvalues(key))

    #dictionary like methods
    def setvalues(self, key:str, *values:str):
        """
        `setvalues`

        A dictionary like get method.

        Sets every value in query with the key `key` to the single given value in `*values`,
        or if multiple `*values` are given,
        then it will set every key in order with a value from `*values`.
        With multiple `*values`, it's expected that the quantity of `*values`
        match the quantity of entries in the query with `key`.
        """
        inds = self.keyindexes(key)

        if len(inds) != len(values) and len(values) != 1:
            raise TypeError(values)

        for vi, qi in enumerate(inds):
            if len(values) != 1:
                value = values[vi]
            else:
                value = values[0]

            self[qi] = (key, value)

    def delkey(self, key:str):
        """
        `delkey`

        Deletes every entry in the query with key `key`.
        """
        for i in reversed(self.keyindexes(key)):
            del self[i]

    def isempty(self) -> bool:
        """
        `isempty`

        Returns:
            `True` if there are no keys or values in this query, otherwise `False`.
        """
        return len(self) <= 0

    def iskeyempty(self, key:str, all_values:bool = False) -> bool:
        """
        `iskeyempty`

        Arguments:
            `key` -- The key to check the value of.

        Keyword Arguments:
            `all_values` -- If `True`, `True` will be returned only if *all* values are empty,
                not just one.
        """
        return (all if all_values else any)(v == "" for v in self.queryvalues(key))

    def encode(self,
               quote: Optional[bool] = None,
               quote_safe:Optional[str] = None,
               force_case: Optional[Literal["upper", "lower", "preserve"]] = None
              ) -> str:
        """
        `encode`

        Keyword Arguments:
            `quoted` -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            `quote_safe` -- If quoting, these characters will be excluded when quoting.
            `force_case` -- If not `None`, the query's case will be converted to the given case, 
                with `None` defaulting to the objects `force_case` attribute for how case should
                be handled.

        Returns:
            This `URIQuery` object, encoded as a string.
        """
        #pylint:disable=unnecessary-lambda-assignment

        if force_case is not None and force_case not in ("upper", "lower", "preserve"):
            raise AttributeError

        if quote is None:
            quote = self.requote

        if force_case is None:
            force_case = self.force_case

        if quote_safe is None:
            quote_safe = self.quote_safe

        qmet = passthrough_first
        if quote:
            qmet = lambda s: uriquote(s, quote_safe)

        cmet = passthrough_first
        if force_case != "preserve":
            cmet = (lambda s: s.upper()) if force_case == "upper" else (lambda s: s.lower())

        quote_via=lambda *p :cmet(qmet(passthrough_first(*p)))
        #we must use items instead of the query dict to ensure that the order remains intace
        encoded = uriqueryunparse(tuple(self.items()), doseq=True, quote_via=quote_via)

        _self_tup = tuple(self.items())
        if len(_self_tup) == 1 and _self_tup[0][0] != "" and _self_tup[0][1] == "":
            #reformat a single, valueless query as just a string of the query key
            encoded = encoded.rstrip("=")

        return encoded
    __str__ = encode
    __repr__ = encode

    def validate(self, encoded:bool = False) -> bool:
        """
        `validate`

        Returns:
            True if all characters in this object are allowed in a URI query.
        """
        if encoded:
            return not CharacterSets.invalid_check(CharacterSets.QUERY, self.encode(True))
        else:
            return not CharacterSets.invalid_check(CharacterSets.QUERY,
                                                   *self.querykeys(),
                                                   *self.queryvalues()
                                                  )

    def search(self,
               keymatch:Optional[Union[str, Pattern]] = None,
               valmatch:Optional[Union[str, Pattern]] = None
              ) -> Iterable[Tuple[Optional[Match], Optional[Match]]]:
        """
        `search`

        Keyword Arguments:
            keymatch -- A optional regex pattern to match keys with.
            valmatch -- A optional regex pattern to match values with.

        Returns:
            An iterable of tuples, each with a match either for a key and/or value,
            with the format of `(Optional[Match], Optional[Match])`,
            the first being matches for keys, the second for values.
        """
        #pylint:disable=unnecessary-lambda, unnecessary-lambda-assignment
        ksch = lambda *a, **k: None
        if isinstance(keymatch, str):
            keymatch = cast(Pattern, regexcompile(keymatch))
        if keymatch is not None:
            ksch = lambda s: keymatch.search(s)

        vsch = lambda *a, **k: None
        if isinstance(valmatch, str):
            valmatch = cast(Pattern, regexcompile(valmatch))
        if valmatch is not None:
            vsch = lambda s: valmatch.search(s)

        return ((ksch(k),vsch(v)) for k,v in self if ksch(k) is not None or vsch(v) is not None)
