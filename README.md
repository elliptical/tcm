[![version](https://img.shields.io/badge/version-1.0.1-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)
[![Build Status](https://travis-ci.org/elliptical/tcm.svg?branch=develop)](https://travis-ci.org/elliptical/tcm)
[![Coverage Status](https://coveralls.io/repos/github/elliptical/tcm/badge.svg?branch=develop)](https://coveralls.io/github/elliptical/tcm?branch=develop)

# tcm (Test Case Meta)
This is primarily an excercise in Python metaprogramming which also lets me see GitHub, CI tools, and PyPI in action.

Things to develop:

- a class method decorator to hold a table of arguments
- a metaclass to automatically generate multiple test methods out of each decorated sample method

Tools to use:

- `tox` to test the code with different Python versions
- `pylint` and `flake8` to keep individual commits clean
- `coverall` to ensure 100% code coverage
