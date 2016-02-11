# -*- coding: utf-8 -*-

import numpy as np


class ChunkedAdapter(object):
    def __init__(self, hdu):
        pass

    def __call__(self, chunksize):
        yield np.zeros((10, 1))
