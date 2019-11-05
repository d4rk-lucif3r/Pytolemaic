import unittest
from examples import example_scoring_report, example_sensitivity_analysis, example_prediction_uncertainty

class TestExamples(unittest.TestCase):

    def test_example_scoring_report(self):
        example_scoring_report.run()

    def test_example_sensitivity_analysis(self):
        example_sensitivity_analysis.run()

    def test_example_prediction_uncertainty(self):
        example_prediction_uncertainty.run()