"""
Test Runner for Python.
"""

import os
import re
from textwrap import dedent
from typing import List
from pathlib import Path
import json
import shutil
import sys

from pylint.lint import Run as PylintRun
import timeout_decorator

from io import StringIO
from .data import Directory, Hierarchy, Results, Test


def find_all(indir):
    test_files = []
    for root, dirs, files in os.walk(indir):
        for file in files:
            if file.endswith(".py"):
                test_files.append(str(Path(root) / file))
    return test_files


def run(
    indir: Directory,
    outdir: Directory,
    max_score: int,
    pylint_args: List[str],
    args: List[str],
) -> None:
    """
    Run the tests for the given exercise and produce a results.json.
    """

    out_file = outdir.joinpath("results.json")

    run_args = []
    run_args = pylint_args.split()

    # run the linter and report

    if "FINDALL" in args:
        args = find_all(indir)

    tests = []
    result = Results()
    result.max_score = max_score

    total_score = 0
    for arg in args:
        pylint_results = PylintRun(run_args + [arg], exit=False).linter.stats
        # print("STATS", pylint_results)

        test = Test(arg)
        test.linter_convention = pylint_results.convention
        test.linter_error = pylint_results.error
        test.linter_fatal = pylint_results.fatal
        test.linter_info = pylint_results.info
        test.linter_refactor = pylint_results.refactor
        test.linter_statement = pylint_results.statement
        test.linter_warning = pylint_results.warning

        test.score += (
            pylint_results.global_note * pylint_results.statement / 10.0 * max_score
        )

        if test.linter_fatal:
            test.fail()

        if test.linter_error:
            test.error()

        tests.append(test)

    total_wight = sum(c.linter_statement for c in tests)
    for test in tests:
        try:
            test.score = test.score / total_wight
            total_score += test.score
        except ZeroDivisionError:
            pass
        result.add(test)

    # print("TOTAL SCORE", total_score)
    # dump the report
    out_file.write_text(result.as_json())
    # remove cache directories
    for cache_dir in [".pytest_cache", "__pycache__"]:
        dirpath = indir / cache_dir
        if dirpath.is_dir():
            shutil.rmtree(dirpath)
