import unittest

import numpy

from pytolemaic.utils.dmd import DMD


class TestDMD(unittest.TestCase):

    def _func(self, x, is_classification):
        y = numpy.sum(x, axis=1) + x[:, 0] - x[:, 1]
        if is_classification:
            y = numpy.round(y, 0).astype(int)
        return y.reshape(-1, 1)

    def get_data(self, is_classification):
        x = numpy.random.rand(1000, 10)

        # 1st is double importance, 2nd has no importance
        y = self._func(x, is_classification=is_classification)
        return DMD(x=x, y=y,
                   columns_meta={DMD.FEATURE_NAMES: ['f_' + str(k) for k in
                                                     range(x.shape[1])]})

    def test_properties(self):
        dmd = self.get_data(is_classification=False)

        self.assertEqual(dmd.n_features, 10)
        self.assertEqual(dmd.n_samples, 1000)
        self.assertTrue(numpy.all(
            dmd.target == self._func(dmd.values, is_classification=False)))

        self.assertListEqual(dmd.feature_names,
                             ['f_' + str(k) for k in range(dmd.n_features)])
