# coding=utf-8
"""
    quick_orm.testsuite
    ~~~~~~~~~~~~~~~~~~~
    unit tests for quick_orm project
"""
import unittest
from quick_orm.testsuite.core import CoreTestCase

def run_testsuite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CoreTestCase))
    unittest.TextTestRunner(verbosity=1).run(test_suite)
