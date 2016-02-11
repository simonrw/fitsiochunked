# -*- coding: utf-8 -*-

from collections import namedtuple


Chunk = namedtuple('Chunk', ['data', 'slice'])

class ChunkedAdapter(object):
    def __init__(self, hdu):
        self.hdu = hdu

    @property
    def nrows(self):
        return self.hdu.get_info()['dims'][0]

    @property
    def num_images(self):
        return self.hdu.get_info()['dims'][1]

    @property
    def data_type(self):
        return self.hdu.get_info()['img_equiv_type']

    @property
    def lc_bytes(self):
        return self._byte_size(self.data_type) * self.num_images

    def __call__(self, chunksize=None, memory_limit_mb=None):
        if chunksize is None and memory_limit_mb is None:
            raise ValueError('You must supply either chunksize or memory_limit_mb arguments')

        start = 0
        end = start + chunksize
        while end <= self.nrows:
            chunk = self.hdu[start:end, :]
            yield Chunk(data=chunk, slice=slice(start, end))

            start += chunksize
            end = min(end + chunksize, self.nrows)
            if start >= end:
                break

    def _byte_size(self, data_type):
        return {
            32: 4,
            -32: 4,
            -64: 8,
        }[data_type]

    def _max_num_lightcurves(self, memory_limit_mb):
        memory_limit_bytes = memory_limit_mb * 1024 * 1024
        return memory_limit_bytes / self._byte_size(self.data_type)

