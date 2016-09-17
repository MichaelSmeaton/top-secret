from src.function_coverage_test import *
from src.statement_coverage_test import *

import unittest


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(FunctionCoverageTests))
    test_suite.addTest(unittest.makeSuite(StatementCoverageTests))

    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    my_suite = suite()
    runner.run(my_suite)
