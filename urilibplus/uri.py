""" 
`uri`

Holds the `URI` class and reated imports.
"""

from urllib.parse import (urlsplit as urisplit,
                          urlunsplit as uriunsplit,
                          quote as uriquote,
                          unquote as uriunquote,
                          unwrap as uriunwrap,
                          SplitResult)
from re import compile as regexcompile

from .characters import CharacterSets
from .uri_path import URIPath
from .uri_query import URIQuery

from .typings import * # pylint: disable=wildcard-import, unused-wildcard-import

class URI:
    """
    `URI`

    A python class used to interact and manipulate with
    uris in python in a easier and consistent manner.
    
    Sources:
     - https://www.rfc-editor.org/rfc/rfc3986
     - https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
    """
    CHARACTER_SETS = CharacterSets

    quotestr = staticmethod(uriquote)
    unquotestr = staticmethod(uriunquote)

    @property
    def authority(self) -> str:
        """
        `authority`

        Returns:
            The authority of the uri;
            ie. the user, password, host, and port;
            formatted as required.
        """
        authority = ""
        if self.user_info != "":
            authority = f"{self.user_info}@"
        authority += f"{self.host}"
        if self.port is not None and self.port > 0:
            authority += f":{self.port}"
        return authority
    @authority.setter
    def authority(self, value: str):
        at_index = value.find("@")
        if at_index < 0:
            self.user_info = ""
        else:
            self.user_info = value[:at_index]
        value = value.replace(self.user_info, "", 1).lstrip("@")

        col_index = value.rfind(":")
        if col_index < 0:
            self.port = None
        else:
            self.port = int(value[col_index+1:])
            if self.port < 0:
                self.port = None
        if self.port is not None:
            value = value.replace(str(self.port), "", 1).rstrip(":")

        self.host = value

    @property
    def username(self) -> Union[None, str]:
        """
        `username`

        Returns:
            The username in the uri, or None if no username in included.
        """
        if self.userinfo.count(":") == 1:
            return self.userinfo[:self.userinfo.find(":")]
        else:
            return None
    @username.setter
    def username(self, value: Union[None, str]):
        if value is None:
            self.userinfo = self.userinfo[self.userinfo.find(":")+1:]
        else:
            if self.userinfo[0] != ":" and self.username is None:
                value += ":"
            self.userinfo = value + \
                self.userinfo[max(self.userinfo.find(":"), 0):]

    @property
    def password(self) -> Union[None, str]:
        """
        `password`

        Returns:
            The password in the uri, or None if no password in included.
        """
        if self.userinfo_string.count(":") == 1:
            return self.userinfo_string[self.userinfo_string.find(":")+1:]
        else:
            return None
    @password.setter
    def password(self, value: Union[None, str]):
        if value is None:
            self.userinfo_string = self.userinfo_string[:self.userinfo_string.find(
                ":")]
        else:
            if self.userinfo_string[-1] != ":" and self.password is None:
                value = ":" + value
            self.userinfo_string = self.userinfo_string[:self.userinfo_string.find(
                ":")] + value

    def __init__(self,
                 contents:Union[str, 'URI', SplitResult, Tuple[str, str, str, str, str]],
                 default_scheme: Optional[str] = None,
                 *,
                 unquote:bool = False,
                 requote:bool = False,
                 quote_safe:str = ""):
        self.scheme: str
        self.user_info: str = ""
        self.host: str = ""
        self.port: Optional[int] = None
        self.path: Optional['URIPath'] = None
        self.query: Optional['URIQuery'] = None
        self.fragment: Optional['URIQuery'] = None

        if default_scheme is None:
            default_scheme = ""

        parsed = None
        if isinstance(contents, SplitResult):
            parsed = contents
        elif isinstance(contents, tuple) and len(contents) <= 5 and len(contents) >= 1:
            parsed = SplitResult(*contents)
        else:
            if isinstance(contents, URI):
                contents = str(contents)
            contents = contents.strip()
            contents = uriunwrap(contents)
            parsed = urisplit(contents, scheme=default_scheme, allow_fragments=True)

        self.scheme = uriunquote(parsed.scheme) if unquote else parsed.scheme
        self.authority = uriunquote(parsed.netloc) if unquote else parsed.netloc
        self.path = URIPath(parsed.path.lstrip("/"), unquote=unquote)
        self.query = URIQuery(parsed.query, unquote=unquote)
        self.fragment = URIQuery(parsed.fragment, unquote=unquote)

        self.default_scheme = default_scheme
        self.requote = requote
        self.quote_safe = quote_safe

    def __repr__(self):
        return f"<URI object (url = {self.encode()}, valid = {self.validate()})>"

    def __len__(self):
        return len(self.encode())

    def __contains__(self, value:str):
        return value in self.encode()

    def __iter__(self):
        return iter(self.tupled())

    def copy(self) -> 'URI':
        """
        `copy`

        Returns:
            A complete, deep, copy of this object.
        """
        return URI(self.splitted(False),
                   default_scheme=self.default_scheme,
                   unquote=False,
                   requote=self.requote,
                   quote_safe=self.quote_safe
                  )
    __copy__ = copy
    __deepcopy__ = copy

    def tupled(self,
               quote: Optional[bool] = None,
               quote_safe:Optional[str] = None
              ) -> Tuple[str, str, str, str, str]:
        """
        `tupled`
        
        Returns this object formated as a `tuple`,
        a ordered in the commonly used order used in native python uri related functions.

        Keyword Arguments:
            quoted -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            This object as a `tuple`.
        """
        if quote is None:
            quote = self.requote

        if quote_safe is None:
            quote_safe = self.quote_safe

        return (uriquote(self.scheme, quote_safe) if quote else self.scheme,
                uriquote(self.authority, quote_safe) if quote else self.authority,
                "" if self.path is None else self.path.encode(quote, quote_safe),
                "" if self.query is None else self.query.encode(quote, quote_safe),
                "" if self.fragment is None else self.fragment.encode(quote, quote_safe)
               )

    def splitted(self,
                 quote: Optional[bool] = None,
                 quote_safe:Optional[str] = None
                ) -> SplitResult:
        """
        `splitted`
        
        Returns this object formated as a `SplitResult`,
        a native object commonly used with native python uri related functions.

        Keyword Arguments:
            quoted -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            This object as a `SplitResult`.
        """
        return SplitResult(*self.tupled(quote, quote_safe))

    def encode(self, quote: Optional[bool] = None, quote_safe:Optional[str] = None) -> str:
        """
        `encode`

        Keyword Arguments:
            quoted -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            The URI object, encoded as a string.
        """

        if quote is None:
            quote = self.requote

        if quote_safe is None:
            quote_safe = self.quote_safe

        encoded = uriunsplit(SplitResult(*self.tupled(None, None)))
        if quote is True:
            encoded = uriquote(encoded, safe = quote_safe)
        elif quote is False:
            encoded = uriunquote(encoded)
        return encoded
    __str__ = encode
    __repr__ = encode

    def stripped(self, quote: Optional[bool] = None, quote_safe:Optional[str] = None) -> str:
        """
        `stripped`

        Keyword Arguments:
            quoted -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            The URI without any fragment or query, ie. the URI with only its
            scheme and authority (host, user, password, and port) and path
        """
        if quote is None:
            quote = self.requote

        if quote_safe is None:
            quote_safe = self.quote_safe

        encoded = uriunsplit(SplitResult(*self.tupled(quote, quote_safe)[:3], "", ""))

        if quote is True:
            encoded = uriquote(encoded, safe = quote_safe)
        elif quote is False:
            encoded = uriunquote(encoded)
        return encoded

    def root(self, quote: Optional[bool] = None, quote_safe:Optional[str] = None) -> str:
        """
        `root`

        Keyword Arguments:
            quoted -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            The URI's root path, ie. the URI with only its
            scheme and authority (host, user, password, and port)
        """
        if quote is None:
            quote = self.requote

        if quote_safe is None:
            quote_safe = self.quote_safe

        encoded = uriunsplit(SplitResult(*self.tupled(quote, quote_safe)[:2], "", "", ""))

        if quote is True:
            encoded = uriquote(encoded, safe = quote_safe)
        elif quote is False:
            encoded = uriunquote(encoded)
        return encoded

    def validate(self) -> bool:
        """
        `validate`

        Returns:
            True if all characters in this object are allowed in a URI.
        """
        for char in self.scheme:
            if char not in self.CHARACTER_SETS.SCHEME:
                return False

        for char in self.user_info:
            if char not in self.CHARACTER_SETS.USERINFO:
                return False

        for char in self.host:
            if char not in self.CHARACTER_SETS.HOST:
                return False

        if not (isinstance(self.port, int) or self.port is None):
            return False

        if self.path is None:
            return False
        elif isinstance(self.path, URIPath) and not self.path.validate():
            return False
        else:
            for char in self.host:
                if char not in self.CHARACTER_SETS.PATH:
                    return False

        if isinstance(self.query, URIQuery) and not self.query.validate():
            return False
        else:
            for char in self.host:
                if char not in self.CHARACTER_SETS.QUERY:
                    return False

        for char in str(self.fragment):
            if char not in self.CHARACTER_SETS.FRAGMENT:
                return False

        # This is specifically stated as invalid in the specs
        if self.authority == "" and self.path[0] == "":
            return False
        return True

    # NOTE this doesn't test all parts fo the URI, just the required parts!
    def isempty(self) -> bool:
        """
        `isempty`

        Returns:
            True if the given url's scheme or path are blank.
        """
        return self.scheme == "" or (self.path is None or self.path.isempty())
    __bool__ = isempty

    def search(self,
               pattern:Union[str, Pattern],
               quoted: Optional[bool] = None,
               quote_safe:Optional[str] = None
              ) -> Optional[Match]:
        """
        `search`

        A simple shorcut to regex `search` this url, returning the `Match`,
        or `None` if there was no matches.

        Arguments:
            `pattern` -- The pattern to check the url with.

        Keyword Arguments:
            quoted -- If not `None`, the URI will be quoted, if `True`; or unquoted, if `False`,
                with `None` defaulting to the objects `quote` attribute.
            quote_safe -- If quoting, these characters will be excluded when quoting.

        Returns:
            `None` if not matches where found, or a `Match` object otherwise.
        """
        if isinstance(pattern, str):
            pattern = regexcompile(pattern)

        return pattern.search(self.encode(quoted, quote_safe))

    def pathappend(self, *parts:Union[str, PathLike]):
        """
        `pathappend`
        
        A simple shorcut to append to the path directly from the this
        object, if a path is defined.
        
        Will initialise `path` if `path` is None.
        
        Arguments:
            `*parts` -- The parts to be appended to the path, in order.
        """
        if self.path is None:
            self.path = URIPath()
        self.path.append(parts)

    def __truediv__(self, value:Union[str, PathLike]) -> 'URI':
        cpy = self.copy()
        cpy.pathappend(value)
        return cpy

    def __floordiv__(self, value:Union[str, PathLike]) -> 'URI':
        cpy = self.copy()
        cpy.pathappend("", value)
        return cpy
