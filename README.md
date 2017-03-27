[![Build Status](https://travis-ci.org/elliptical/tcm.svg?branch=develop)](https://travis-ci.org/elliptical/tcm)

# tcm (Test Case Meta)
This is primarily an excercise in Python metaprogramming which also lets me see github and CI tools in action.

Things to develop:
* a class method decorator to hold a table of arguments
* a metaclass to automatically generate multiple test methods out of each decorated sample method

Tools to use:
* tox to test the code with different Python versions
* pylint and flake8 to keep individual commits clean
