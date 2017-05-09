Sailfish Setup
==============

This package is responsible for creating Sailfish OS specific users and/or groups on which
other packages could depend on.

Usage
-----

A package that requires that Sailfish OS specific users and/or groups are
already created should have following prerequisite:
Requires(pre): sailfish-setup
