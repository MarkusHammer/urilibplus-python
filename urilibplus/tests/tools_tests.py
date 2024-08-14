""" 
`tools_tests`

Holds tests that relate to tool functions and classes.
"""

import unittest
from string import ascii_letters
from random import choice, randrange
from urilibplus.tools import singlify_str, passthrough_first, absindex, slice_to_range, iter_flatten
from urilibplus.typings import * #pylint:disable=wildcard-import, unused-wildcard-import

class TestStringSinglify(unittest.TestCase):
    """
    `TestStringSinglify`

    Test cases for the `singlify_str` tool function.
    """

    def make_random_string(self, length:int = 1, random_repeat_range:range = range(1,1)) -> str:
        """
        `make_random_string`

        Used to generate a strign of random ascii characters.

        Keyword Arguments:
            length -- The target length of the returned string (before repetition).
            random_repeat_range -- A `range` object that contains all
                possible amounts of times a character should be repeated in a string.

        Returns:
            A string of random characters with a length of *at least* `length`.
        """
        return "".join(choice(ascii_letters) * choice(random_repeat_range) for _ in range(length))

    def test_removes_duplicates(self):
        """
        `test_removes_duplicates`
        
        Tests that `singlify_str` removes all duplacate characters from a string.
        """
        target_lengths = list(range(0,6))
        target_lengths +=  list(range(0,250,10))
        target_lengths += list(2**x for x in range(0,8))
        target_lengths += list(randrange(0,1000) for _ in range(25))

        for length in set(target_lengths):
            test_str = cast(LiteralString, self.make_random_string(length, range(2,5)))
            if test_str == "":
                self.assertEqual(singlify_str(test_str), test_str)
            else:
                self.assertNotEqual(singlify_str(test_str), test_str)

    EXAMPLES = {
        "AAbBVvvCccccd" : "AbBVvCcd",
        "abcdefg" : "abcdefg",
        "bbbbaaabbbbyyyyy" : "bay",
        "!?!?!?!?!" : "!?",
        "oh, what lovely tests...": "oh, watlveys."
    }
    def test_example_deduplication(self):
        """
        `test_example_deduplication`
        
        Used to test that `singlify_str` converts strings into a expected
        output by using examples.
        """
        for ex_in, ex_out in TestStringSinglify.EXAMPLES.items():
            self.assertEqual(set(singlify_str(cast(LiteralString, ex_in))), set(ex_out))

class TestPassthroughFirst(unittest.TestCase):
    """
    `TestPassthroughFirst`

    Test cases for the `passthrough_first` tool function.
    """

    def test_passthrough(self):
        """
        `test_passthrough`
        
        Tests that `passthrough_first` only returns the first argument, unmodified;
        using hardcoded examples.
        """
        self.assertEqual(passthrough_first(*tuple(range(0,10))), 0)
        self.assertEqual(passthrough_first(0, 1, 2, 3, 4), 0)
        self.assertEqual(passthrough_first(0), 0)

class AbsIndexTests(unittest.TestCase):
    """
    `AbsIndexTests`

    Tests the `absindex` tool function.
    """

    def test_random_range(self):
        """
        `test_random_range`
        
        Tests that `absindex` return roughly sane values with random inputs.
        """

        for _ in range(5000):
            length = randrange(1, 1000000)

            index = randrange(-(length + 1), length)
            absind = absindex(index, length)
            self.assertGreaterEqual(absind, 0)
            self.assertLess(absind, length)

    def test_random_range_drifting(self):
        """
        `test_random_range_drifting`
        
        Similar to `test_random_range`, but repeatedly tests that a random value,
        when fed back into `absindex` returns the same index.
        """

        for _ in range(500):
            length = randrange(1, 1000000)
            index = randrange(-(length + 1), length)
            absind = absindex(index, length)
            for _ in range(randrange(5, 10)):
                temp_absind = absindex(absind, length)
                self.assertEqual(absind, temp_absind)
                absind = temp_absind

    def test_positive_index(self):
        """
        `test_positive_index`
        
        Ensures that positive indexes are properly preserved
        when inputted.
        """
        for _ in range(5000):
            length = randrange(1, 1000000)
            index = randrange(0, length)
            absind = absindex(index, length)
            self.assertEqual(absind, index)

    def test_negative_index(self):
        """
        `test_negative_index`
        
        Ensures that negative indexes are properly converted
        to their positive counterpart with `absindex` by using random values.
        """

        for _ in range(5000):
            length = randrange(1, 1000000)
            index = randrange(-length, -1)
            absind = absindex(index, length)
            self.assertEqual(absind, length + index)

class TestSliceToRange(unittest.TestCase):
    """
    `TestSliceToRange`

    Test cases for the `slice_to_range` tool function.
    """

    def test_direct(self):
        """
        `test_direct`
        
        Tests that `slice_to_range` converts slices to ranges as expected,
        using a single hardcoded slice with a random, but valid, reference length.
        """
        testlength = randrange(10,50)
        trange = slice_to_range(slice(1,9,5), testlength)
        self.assertEqual(trange, range(1,9,5))

    def test_negative_wrap(self):
        """
        `test_direct`
        
        Tests that `slice_to_range` converts slices with negative values to ranges as expected;
        using a single hardcoded slice with a random, but valid, reference length.
        """
        testlength = randrange(10,50)
        trange = slice_to_range(slice(-1,-9,2), testlength)
        self.assertEqual(trange, range(testlength-1,testlength-9-1,5))

class TestIterFlatten(unittest.TestCase):
    """
    `TestIterFlatten`

    Test cases for the `iter_flatten` tool function.
    """

    def assertIterEqual(self, i1:Iterable, i2:Iterable): #pylint:disable=invalid-name
        """
        `assertIterEqual`

        Asserts that the two iterables contain the exact same objects,
        and the same amount of said objects.
        """
        self.assertTupleEqual(tuple(i1), tuple(i2))

    def test_direct(self):
        """
        `test_direct`
        
        Tests that `iter_flatten` iterates the same as its input if
        there are no iterable objects yielded from the input;
        with a single hardcoded example.
        """
        self.assertIterEqual(iter_flatten((1,2,3,4,5)), (1,2,3,4,5))

    def test_flatten(self):
        """
        `test_flatten`
        
        Tests that `iter_flatten` iterates a flat iterable if
        the input is a iterable containing some other iterable objects, recursively;
        with a couple hardcoded examples.
        """
        self.assertIterEqual(iter_flatten((1,(2,3),(4,5))), (1,2,3,4,5))
        self.assertIterEqual(iter_flatten((((1,(2,3)),(4,5)))), (1,2,3,4,5))

    def test_flatten_except(self):
        """
        `test_flatten_except`
        
        Tests that `iter_flatten` iterates a flat iterable, but excluding the given types if
        the input is a iterable containing some other iterable objects, recursively;
        with a couple hardcoded examples.
        """

        flat1 = iter_flatten((1, "two", 3, "four", 5, True), str)
        self.assertIterEqual(flat1, (1, "two", 3, "four", 5, True))
        flat2 = iter_flatten((((1, "two"), (3, ("four", 5, True)))), str)
        self.assertIterEqual(flat2, (1, "two", 3, "four", 5, True))
        flat3 = iter_flatten((((1, "two"), (3, ("four", 5, True)))))
        self.assertIterEqual(flat3, (1, "t", "w", "o", 3, "f", "o", "u", "r", 5, True))

if __name__ == '__main__':
    unittest.main()
