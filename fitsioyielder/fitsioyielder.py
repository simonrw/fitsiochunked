# -*- coding: utf-8 -*-

import numpy as np


class ChunkedAdapter(object):
    def __init__(self, hdu):
        self.hdu = hdu

    @property
    def nrows(self):
        return self.hdu.get_info()['dims'][0]

    def __call__(self, chunksize):
        start = 0
        end = start + chunksize
        while end <= self.nrows:
            chunk = self.hdu[start:end, :]
            yield chunk

            start += chunksize
            end = min(end + chunksize, self.nrows)
            if start >= end:
                break


