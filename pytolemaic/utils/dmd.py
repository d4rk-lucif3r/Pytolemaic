import copy

import numpy as np
import pandas


class ShuffleSplitter():
    @classmethod
    def split(cls, dmdy, ratio=0.1, random_state=0):
        n_right = int(np.round(dmdy.n_samples * ratio, 0))
        rs = np.random.RandomState(random_state)
        shuffled = rs.permutation(dmdy.n_samples)
        return shuffled[:-n_right], shuffled[-n_right:]


class DMD():
    FEATURE_NAMES = '__FEATURE_NAMES__'
    INDEX = '__INDEX__'

    # SAMPLE_WEIGHTS = '__SAMPLE_WEIGHTS__'

    def __init__(self, x, y=None, columns_meta=None, samples_meta=None,
                 splitter=ShuffleSplitter):

        self._x = pandas.DataFrame(x)
        if y is not None:
            self._y = pandas.DataFrame(y)
        else:
            self._y = None

        self._columns_meta = self._create_columns_meta(columns_meta, self._x)
        self._samples_meta = self._create_samples_meta(samples_meta, self._x)
        self._splitter = splitter

    @classmethod
    def _create_columns_meta(cls, columns_meta, df):
        if columns_meta is None:
            columns_meta = pandas.DataFrame({DMD.FEATURE_NAMES: df.columns})
        else:
            columns_meta = pandas.DataFrame(columns_meta)

        if DMD.FEATURE_NAMES not in columns_meta:
            columns_meta[DMD.FEATURE_NAMES] = df.columns
        return columns_meta

    @classmethod
    def _create_samples_meta(cls, samples_meta, df):
        if samples_meta is None:
            samples_meta = pandas.DataFrame(
                {DMD.INDEX: np.arange(df.shape[0])})
        else:
            samples_meta = pandas.DataFrame(samples_meta)

        if DMD.INDEX not in samples_meta:
            samples_meta[DMD.INDEX] = np.arange(df.shape[0])
        return samples_meta

    def split_by_indices(self, indices):
        return DMD(x=copy.deepcopy(self._x.iloc[indices, :]),
                   y=copy.deepcopy(self._y.iloc[indices, :]),
                   columns_meta=copy.deepcopy(self._columns_meta),
                   samples_meta=copy.deepcopy(
                       self._samples_meta.iloc[indices, :]),
                   splitter=self.splitter)

    def split(self, ratio):

        dmd_y = DMD(x=self._y.values if self._y is not None else np.arange(
            self.n_samples), samples_meta=self._samples_meta)
        left, right = self.splitter.split(dmd_y, ratio=ratio)
        left = list(sorted(left))
        right = list(sorted(right))

        return self.split_by_indices(left), self.split_by_indices(right),

    @property
    def feature_names(self):
        return list(self._columns_meta[DMD.FEATURE_NAMES])

    @property
    def shape(self):
        return self._x.shape

    @property
    def n_samples(self):
        return self.shape[0]

    @property
    def n_features(self):
        return self.shape[1]

    @property
    def index(self):
        return self._samples_meta[DMD.INDEX]

    @property
    def values(self):
        return self._x.values

    @property
    def target(self):
        if self._y is None:
            return None
        else:
            return self._y.values.reshape(-1, 1)

    @property
    def splitter(self):
        return self._splitter
