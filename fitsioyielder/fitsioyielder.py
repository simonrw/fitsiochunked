# -*- coding: utf-8 -*-

from contextlib import contextmanager

@contextmanager
def open(filename):
    yield Yielder()

class Yielder(object):
    pass
