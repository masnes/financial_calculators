'''
tests for cagr calculator
By: Michael Asnes
'''
import unittest
import cagr

class TestCases(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_div_zero(self):
        zero_begginning_value = cagr.cagr(1, 0, 1)
        zero_periods = cagr.cagr(1, 1, 0)
