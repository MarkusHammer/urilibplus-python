"""
characters

Holds the character literals and related functions for the `urilibplus` module.
"""

from urllib.parse import scheme_chars as uri_scheme_chars
from string import ascii_letters, digits, hexdigits

from .typings import * # pylint: disable=wildcard-import, unused-wildcard-import
from .tools import singlify_str

class CharacterSets:
    """
    `CharacterSets`

    Holds the character literals and related functions for the `urilibplus` module.
    
    Sources:
     - https://www.rfc-editor.org/rfc/rfc3986
     - https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
    """

    HEXDIGITS: LiteralString = hexdigits
    DIGITS: LiteralString = digits
    LETTERS: LiteralString = ascii_letters

    GENERIC_DELIMITERS: LiteralString = ":/?#[]@"
    SPECIFIC_DELIMITERS: LiteralString = "!$&'()*+,;="
    PERCENT_ENCODING: LiteralString = singlify_str(HEXDIGITS,
                                                   "%")
    UNRESERVED: LiteralString = singlify_str(LETTERS,
                                             DIGITS,
                                             "-._~")
    P_CHARS: LiteralString = singlify_str(UNRESERVED,
                                          PERCENT_ENCODING,
                                          SPECIFIC_DELIMITERS,
                                          ":@")
    ALL: LiteralString = singlify_str(GENERIC_DELIMITERS,
                                      SPECIFIC_DELIMITERS,
                                      PERCENT_ENCODING,
                                      UNRESERVED)

    SEGMENT: LiteralString = P_CHARS

    SCHEME: LiteralString = cast(LiteralString, uri_scheme_chars)
    USERINFO: LiteralString = singlify_str(UNRESERVED,
                                           PERCENT_ENCODING,
                                           SPECIFIC_DELIMITERS,
                                           ":")
    HOST: LiteralString = singlify_str(DIGITS,
                                       HEXDIGITS,
                                       UNRESERVED,
                                       PERCENT_ENCODING,
                                       SPECIFIC_DELIMITERS,
                                       ".-:[]")
    PORT: LiteralString = DIGITS
    PATH: LiteralString = singlify_str(SEGMENT, "/")
    QUERY: LiteralString = singlify_str(P_CHARS, "/?")
    FRAGMENT: LiteralString = QUERY

    @staticmethod
    def invalid_check(character_set: LiteralString, *validate_all: str) -> bool:
        """
        `invalid_check`

        Checks that all the `*validate_all` strings only use
        characters from the given `character-set`

        Arguments:
            `character_set` -- The character set to check the strings with.
            `*validate_all` -- The strings to check.

        Returns:
            True if *all* `*validate_all` strings only use
            the characters in the given `character_set`.
        """

        return any(any((c not in character_set) for c in s) for s in validate_all if s != "")
