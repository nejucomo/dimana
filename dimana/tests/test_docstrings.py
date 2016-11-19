import unittest
import doctest


class DocTests (unittest.TestCase):
    def test_docstrings(self):
        doctest.testfile('../../README.rst')
