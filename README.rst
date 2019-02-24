|version| |license| |Build Status| |Coverage Status|

tcm (Test Case Meta)
====================

This is primarily an excercise in Python metaprogramming which also lets
me see github and CI tools in action.

Things to develop:

-  a class method decorator to hold a table of arguments
-  a metaclass to automatically generate multiple test methods out of
   each decorated sample method

Tools to use:

-  tox to test the code with different Python versions
-  pylint and flake8 to keep individual commits clean

.. |version| image:: https://img.shields.io/badge/version-1.0.0-blue.svg
   :target: ./CHANGELOG.md
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE.md
.. |Build Status| image:: https://travis-ci.org/elliptical/tcm.svg?branch=develop
   :target: https://travis-ci.org/elliptical/tcm
.. |Coverage Status| image:: https://coveralls.io/repos/github/elliptical/tcm/badge.svg?branch=develop
   :target: https://coveralls.io/github/elliptical/tcm?branch=develop
