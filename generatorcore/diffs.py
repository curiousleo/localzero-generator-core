"""Module diffs -- Utility module to compare to result dictionaries.

During testing and development it is often necessary to compare two result dictionaries.
"""
from dataclasses import dataclass
import collections.abc
import math
import numbers
import typing


def float_matches(actual, expected, rel):
    if math.isnan(actual) and math.isnan(expected):
        return True
    elif math.isnan(actual):
        return False
    elif math.isnan(expected):
        return False
    reltol = math.fabs(expected) * rel
    diff = math.fabs(actual - expected)
    if diff < reltol:
        return True
    if diff < 1e-12:
        return True
    return False


class MissingSentinel:
    def __str__(self):
        return "nothing"


MISSING_SENTINEL = MissingSentinel()


@dataclass
class Diff:
    path: str
    actual: object
    expected: object

    def __str__(self) -> str:
        return f"at {self.path} expected {self.expected} got {self.actual}"


def all_helper(path: str, actual, expected, *, rel) -> typing.Iterator[Diff]:
    if isinstance(actual, collections.abc.Mapping) and isinstance(
        expected, collections.abc.Mapping
    ):
        keys1 = frozenset(actual.keys())
        keys2 = frozenset(expected.keys())
        shared_keys = keys1.intersection(keys2)
        for k in shared_keys:
            yield from all_helper(path + "." + k, actual[k], expected[k], rel=rel)
        for k in keys1 - shared_keys:
            yield from all_helper(path + "." + k, actual[k], MISSING_SENTINEL, rel=rel)
        for k in keys2 - shared_keys:
            yield from all_helper(
                path + "." + k, MISSING_SENTINEL, expected[k], rel=rel
            )
    elif isinstance(actual, collections.abc.Mapping) and expected is MISSING_SENTINEL:
        for k in actual.keys():
            yield from all_helper(path + "." + k, actual[k], MISSING_SENTINEL, rel=rel)
    elif isinstance(expected, collections.abc.Mapping) and actual is MISSING_SENTINEL:
        for k in expected.keys():
            yield from all_helper(
                path + "." + k, MISSING_SENTINEL, expected[k], rel=rel
            )
    elif isinstance(actual, numbers.Number) and isinstance(expected, numbers.Number):
        if not float_matches(actual=actual, expected=expected, rel=rel):
            yield Diff(path=path, actual=actual, expected=expected)
    elif actual != expected:
        yield Diff(path=path, actual=actual, expected=expected)


def all(*, actual, expected, rel=1e-9):
    return all_helper("", actual, expected, rel=rel)
