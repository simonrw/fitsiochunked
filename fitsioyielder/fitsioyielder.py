# -*- coding: utf-8 -*-

from contextlib import contextmanager

@contextmanager
def open(filename):
    yield Yielder()

class Yielder(object):
    def __init__(self):
        self.fitsio = None

    def __getitem__(self, key):
        return HDU()

class HDU(object):
    def __init__(self):
        self.hdu = None

    def chunks(self, chunksize):
        pass
