""" 
`tools`

Holds various tool and utility functions and classes for `urilibplus`.
"""

from .typings import * #type:ignore # pylint: disable=wildcard-import, unused-wildcard-import

def singlify_str(*in_strs: LiteralString) -> LiteralString:
    """
    `singlify_str`

    Arguments:
        `*in_strs` -- All strings to concatenate and singlify together.

    Returns:
        All `*in_strs` concatenated, with any duplicate characters removed, in no particular order.
    """
    return cast(LiteralString, "".join(set("".join(in_strs))))

@overload
def passthrough_first() -> NoReturn: ...
@overload
def passthrough_first(*p:Any, **_) -> Any: ... #type:ignore
def passthrough_first(*p:Any, **_) -> Union[Any, NoReturn]: #pylint:disable=inconsistent-return-statements
    """
    `passthrough_first`

    A simple function for use in filtering and sorting.
    Takes in any amount of args and kwargs, returning only the first arg given.

    Arguments:
        `*p` -- Any amount of arguments, with only the first one given passed through.

    Returns:
        Only the first argument passed to this function.
    """
    if len(p) > 0:
        return p[0]

def absindex(index:int, reference_length:Union[Sized, int]) -> int:
    """
    `absindex`

    Takes the given index and the legnth contex its
    used in and returns a absolute index that
    wraps a negative index into a positive one while
    throwing relevant errors for out of bounds indexes.

    Arguments:
        index -- The index in question.
        reference_length -- The length of the object being sliced, or the `Sized` object itself.

    Raises:
        ValueError: Raised when an erroneous length is given.
        IndexError: Raised when the given index is / would be out of bounds.

    Returns:
        The absolute index (will never be negative).
    """

    length:int = 0
    if isinstance(reference_length, int):
        length = reference_length
    else:
        length = len(reference_length)

    if length < 0:
        raise ValueError(length)
    if index + length < 0:
        raise IndexError(index)

    return index if index >= 0 else length + index

def slice_to_range(sl:slice, reference_length:Union[Sized, int]) -> range:
    """
    `slice_to_range`
    
    Used to convert a `slice` object into a `range` object.

    Arguments:
        sl -- The source slice to convert.
        reference_length -- The length of the object being sliced, or the `Sized` object itself.

    Returns:
        The generated range from the slice.
    """

    length:int = 0
    if isinstance(reference_length, int):
        length = reference_length
    else:
        length = len(reference_length)

    if length < 0:
        raise IndexError("The reference length was negative")

    start = (absindex(sl.start, length) if (sl.start is not None) else 0)
    stop = (absindex(sl.stop, length) if (sl.stop is not None) else length)
    step = (sl.step if (sl.step is not None) else (1 if (start < stop) else -1))

    return range(start, stop, step)

def iter_flatten(it:Iterable[Union[Any,Iterable[Any]]],
                 *excepttypes:type,
                 only_self_iterate_guard:bool = True
                ) -> Iterator[Any]:
    """
    `iter_flatten`
    
    'Flattens' a given iterable, meaning that it will return a iterator that when iterated, will
    yield every object from input iterator, unless that given object is an iterable,
    in which case it will first iterate fully though that iterable fully before
    continuing to iterate through the original input iterator; recursively.

    Arguments:
        `it` -- The iterator to flatten recursively.
        `*excepttypes` -- When encountering this type in an iterable,
            it will never be iterated itself, instead being yielded whole.
        `only_self_iterate_guard` -- When `True`, any iterable object that only yields
            a single object which is equal to itself, it will not be iterated further,
            instead begin yielded.
            This is used to guard infinite iteration with objects that allow
            for themselves to be iterated even when they only contain
            a single object - such as strings.
            It is heavily advised to leave this `True`, unless it is explicitly
            causing issues with a certian use case.

    Yields:
        The object of the input iterable, and any objects within iterables in that initial iterator.
    """
    for x in it:
        iter_this:bool = isinstance(x, Iterable) and (not isinstance(x, excepttypes))
        if iter_this and only_self_iterate_guard:
            tupled = tuple(cast(Iterable, x))
            iter_this = not(len(tupled) == 1 and tupled[0] == x)

        if iter_this:
            yield from iter_flatten(cast(Iterable, x),
                                      *excepttypes,
                                      only_self_iterate_guard=only_self_iterate_guard
                                     )
        else:
            yield x
