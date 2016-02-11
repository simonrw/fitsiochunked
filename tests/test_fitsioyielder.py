#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fitsioyielder
----------------------------------

Tests for `fitsioyielder` module.
"""

import pytest
from fitsioyielder import fitsioyielder

@pytest.fixture
def filename():
    return 'test.fits'

def test_open(filename):
    with fitsioyielder.open(filename) as infile:
        assert isinstance(infile, fitsioyielder.Yielder)

def test_yielder_has_fitsio_object(filename):
    with fitsioyielder.open(filename) as infile:
        assert hasattr(infile, 'fitsio')

def test_can_get_hdu(filename):
    with fitsioyielder.open(filename) as infile:
        assert isinstance(infile['flux'], fitsioyielder.HDU)


'''
Expected API

with fitsioyielder.open(filename) as infile:
    for chunk in infile['flux'].chunks(chunksize=10):
        # do something with chunk
'''
