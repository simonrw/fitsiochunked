#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fitsioyielder
----------------------------------

Tests for `fitsioyielder` module.
"""

import pytest
import fitsio
import numpy as np
from fitsioyielder import fitsioyielder

@pytest.fixture(scope='session')
def filename():
    return 'test.fits'

@pytest.fixture(scope='session')
def data():
    return np.random.randint(0, 10, size=(100, 50))


@pytest.fixture
def hduname():
    return 'flux'


@pytest.yield_fixture
def hdulist(filename, tmpdir, data, hduname):
    fname = str(tmpdir.join(filename))
    with fitsio.FITS(fname, 'rw', clobber=True) as outfile:
        outfile.write(data, extname=hduname)
        yield outfile

@pytest.fixture
def chunker(hdulist, hduname):
    hdu = hdulist[hduname]
    return fitsioyielder.ChunkedAdapter(hdu)


def test_number_of_rows(chunker):
    assert chunker.nrows == 100


def test_chunk_size(chunker):
    next_chunk = next(chunker(chunksize=10))
    assert next_chunk.shape[0] == 10


@pytest.mark.parametrize('chunksize,nchunks', [
    (50, 2),
    (100, 1),
    (10, 10),
    (1, 100),
    (99, 2),
])
def test_number_of_chunks(chunker, chunksize, nchunks):
    chunks = list(chunker(chunksize=chunksize))
    assert len(chunks) == nchunks


@pytest.mark.parametrize('chunksize', [
    50, 100, 10, 1, 99
])
def test_chunk_contents(chunker, data, chunksize):
    chunks = list(chunker(chunksize=chunksize))
    for i in range(len(chunks)):
        assert (chunks[i] == data[i * chunksize: (i + 1) * chunksize]).all()


def test_uneven_chunks(chunker):
    chunksize=99
    chunks = list(chunker(chunksize=chunksize))
    assert chunks[0].shape[0] == 99
    assert chunks[1].shape[0] == 1


'''
Expected API

with fitsio.FITS(filename) as infile:
    hdu = infile['flux']
    chunker = fitsioyielder.ChunkedAdapter(hdu)
    for chunk in chunker(chunksize=10): # or chunker(memory_limit=2048)
        # do something with chunk
'''
