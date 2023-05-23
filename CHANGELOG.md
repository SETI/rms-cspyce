# Change Log
All notable changes to `cspyce` will be documented here

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project tries to adhere to [Semantic Versioning](http://semver.org/).

## [2.1.1] - 2023-05-23
Fix various memory corruption issues that caused crashing under MacOS.
Fix implementation issues with `dafgda`, `dafus`, `dasrdc`, `dp2hx`,
and `dskd02`.

## [2.1.0] - 2023-05-04
Stable release using new release process. Remove all Python 2 support.
Add `cspyce.__version__` attribute. Fix bug with converting longlong to float
on Windows. Fix bug in `ckfxfm` where it was calling the wrong underlying
CSPICE function.

## [2.0.10 thru 2.0.11] - 2023-05-03
Convert LICENSE.txt to LICENSE.md. Improvements to release process and
documentation. Fix bug in `ckw01` and failing typemap tests.

## [2.0.9] - 2023-04-19
Fix minor bug in aliases, fix lmpool, fix problems with array support.
Add LICENSE.txt.

## [2.0.6 thru 2.0.8] - 2022-11-03
Improvements to release process.

## [2.0.5] - 2022-10-13
Fix crashes in aliases, improve docstrings, fix memory allocation errors.
Reorganize and add test cases.

## [2.0.4] - 2022-08-12
Fix crash in aliases, fix to work with Python 2.

## [2.0.3] - 2022-04-14
Major internal reorganization.

## [2.0.2] - 2022-03-21
Download the appropriate version of the CSPICE sources depending on
the architecture.

## [2.0.1] - 2022-03-21
Minor bug fixes.

## [2.0.0] - 2022-03-17
Internal rearrangement to support both Python 2 and Python 3 and also allow
installation with `pip`.
