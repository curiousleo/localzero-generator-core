#!/usr/bin/env python
"""
This is a simple wrapper around the generator to

    - Make sure we eat our own dogfood(TM) and try the API.

    - Give us a quick way to run the generator as
      just running Generator.py as a script runs into the
      scripts and packages / modules shall not be mixed rule.
      See https://mail.python.org/pipermail/python-3000/2007-April/006793.html
"""
import argparse
import json
import sys
import collections.abc
import typing
import numbers
import pytest
import os.path
from generatorcore.generator import calculate_with_default_inputs
from generatorcore import refdatatools
from generatorcore import refdata


def run_cmd(args):
    # TODO: pass ags in here
    g = calculate_with_default_inputs(ags=args.ags, year=args.year)
    json.dump(g.result_dict(), indent=4, fp=sys.stdout)


def sanitize_excel(e):
    """We are not interested in string values and some odd keys can be thrown away too"""
    if isinstance(e, dict):
        return {
            k: sanitize_excel(v)
            for k, v in e.items()
            if k != "\u00a0" and not isinstance(v, str)
        }
    else:
        return e


def remove_null_values(r):
    """Because of the way we have declared types we produce too many values."""
    if isinstance(r, dict):
        return {k: v for k, v in r.items() if v is not None}
    else:
        return r


def find_diffs(
    path: str, d1, d2, *, rel
) -> typing.Iterator[tuple[str, typing.Any, typing.Any]]:
    if isinstance(d1, collections.abc.Mapping) and isinstance(
        d2, collections.abc.Mapping
    ):
        keys1 = frozenset(d1.keys())
        keys2 = frozenset(d2.keys())
        shared_keys = keys1.intersection(keys2)
        for k in shared_keys:
            yield from find_diffs(path + "." + k, d1[k], d2[k], rel=rel)
        for k in keys1 - shared_keys:
            yield from find_diffs(path + "." + k, d1[k], None, rel=rel)
        for k in keys2 - shared_keys:
            yield from find_diffs(path + "." + k, None, d2[k], rel=rel)
    elif isinstance(d1, collections.abc.Mapping) and d2 is None:
        for k in d1.keys():
            yield from find_diffs(path + "." + k, d1[k], None, rel=rel)
    elif isinstance(d2, collections.abc.Mapping) and d1 is None:
        for k in d2.keys():
            yield from find_diffs(path + "." + k, None, d2[k], rel=rel)
    elif isinstance(d1, numbers.Number) and isinstance(d2, numbers.Number):
        if d1 != pytest.approx(d2, rel=rel, nan_ok=True):
            yield (path, d1, d2)
    elif d1 != d2:
        yield (path, d1, d2)


def compare_to_excel_cmd(args):
    def pr3(a, b, c):
        if b is None:
            b = "MISSING"
        elif b == {}:
            b = "{}"
        if c is None:
            c = "MISSING"
        elif c == {}:
            c = "{}"
        print(f"{a:<50}{b:>25}{c:>25}")

    with open(args.result_file) as fp:
        result = remove_null_values(json.load(fp))
    with open(args.excel_file) as fp:
        excel = sanitize_excel(json.load(fp))
    diffs = find_diffs("", result, excel, rel=float(args.relative_tolerance))
    if diffs:
        pr3("PATH", "RESULT", "EXCEL")
        for (p, r, x) in diffs:
            if args.show_missing_in_excel or x != None:
                pr3(p, r, x)


def data_check_repos_cmd(args):
    ds = refdatatools.DataDirStatus.get(refdatatools.datadir())
    # TODO: Add a verbose option that prints a json of DataDirStatus
    if not ds.is_good():
        exit(1)


def data_checkout_cmd(args):
    datadir = refdatatools.datadir()
    production = refdata.Version.load("production", datadir=datadir)
    status: refdatatools.DataDirStatus | None = None
    status_error = None
    freshly_cloned = False
    try:
        # This means we are loading the version file twice. Which is a bit
        # silly but oh well...
        status = refdatatools.DataDirStatus.get(datadir)
    except Exception as e:
        status_error = e

    public_dir = os.path.join(datadir, "public")
    proprietary_dir = os.path.join(datadir, "proprietary")

    if status is None:
        assert status_error is not None
        if not os.path.exists(public_dir) and not os.path.exists(proprietary_dir):
            print(
                "Looks like there is no checkout at all yet -- cloning for you",
                file=sys.stderr,
            )
            refdatatools.clone(datadir, "public")
            refdatatools.clone(datadir, "proprietary")
            # Retry getting the status. If this fails now, we are in some screwed up state anyway
            status = refdatatools.DataDirStatus.get(datadir)
            freshly_cloned = True
        else:
            print(
                f"Hmm there already seems to be directories for the data repos, but data check-repos failed with {status_error}. Giving up..."
            )
            exit(1)
    else:
        # make sure we are not causing data loss
        if not status.public_status.is_clean or not status.proprietary_status.is_clean:
            print(
                "There uncommitted changes or untracked files in at least one data repository. Fix that first."
            )
            exit(1)

    if status is not None and status.public_status.rev == production.public:
        if not freshly_cloned:
            print(
                f"public already contains a checkout of {production.public} -- not touching it",
                file=sys.stderr,
            )
    else:
        refdatatools.checkout(datadir, "public", production.public)

    if status is not None and status.proprietary_status.rev == production.proprietary:
        if not freshly_cloned:
            print(
                f"proprietary already contains a checkout of {production.proprietary} -- not touching it",
                file=sys.stderr,
            )
    else:
        refdatatools.checkout(datadir, "proprietary", production.proprietary)


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults()
    subcmd_parsers = parser.add_subparsers(dest="subcmd")

    cmd_run_parser = subcmd_parsers.add_parser("run", help="Run the generator")
    cmd_run_parser.add_argument("-ags", default="03159016")
    cmd_run_parser.add_argument("-year", default=2035)
    cmd_run_parser.set_defaults(func=run_cmd)

    cmd_compare_to_excel_parser = subcmd_parsers.add_parser(
        "compare_to_excel", help="Compare an end to end test file with an excel file"
    )
    cmd_compare_to_excel_parser.add_argument("result_file")
    cmd_compare_to_excel_parser.add_argument("excel_file")
    cmd_compare_to_excel_parser.add_argument(
        "-show-missing-in-excel", action="store_true"
    )
    cmd_compare_to_excel_parser.add_argument(
        "-relative-tolerance", action="store", default="1e-6"
    )
    cmd_compare_to_excel_parser.set_defaults(func=compare_to_excel_cmd)

    cmd_data_check_repos = subcmd_parsers.add_parser(
        "check-repos",
        help="Check that the data dir contains clean checkouts of the production reference data set",
    )
    cmd_data_check_repos.set_defaults(func=data_check_repos_cmd)

    cmd_data_checkout = subcmd_parsers.add_parser(
        "checkout",
        help="Checkout the production version of the data repositories (if necessary clone them first)",
    )
    cmd_data_checkout.set_defaults(func=data_checkout_cmd)
    args = parser.parse_args()
    if args.subcmd is None:
        parser.print_help()
    else:
        args.func(args)


main()
