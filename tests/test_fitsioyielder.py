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


def test_number_of_rows(chunker, data):
    assert chunker.nrows == data.shape[0]


def test_number_of_images(chunker, data):
    assert chunker.num_images == data.shape[1]


def test_data_type(chunker):
    assert chunker.data_type == 32


def test_chunk_size(chunker):
    next_chunk, _ = next(chunker(chunksize=10))
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
        assert (chunks[i][0] == data[i * chunksize: (i + 1) * chunksize]).all()


def test_uneven_chunks(chunker):
    chunksize=99
    chunks = list(chunker(chunksize=chunksize))
    assert chunks[0][0].shape[0] == 99
    assert chunks[1][0].shape[0] == 1


@pytest.mark.parametrize('dtype_size, expected', [
    (32, 4),
    (-32, 4),
    (-64, 8),
])
def test_get_image_data_type_size(chunker, dtype_size, expected):
    assert chunker._byte_size(dtype_size) == expected


def test_get_lc_size(chunker, data):
    assert chunker.lc_bytes == data.shape[1] * 4


def test_error_with_no_chunksize_or_memory_limit(chunker):
    with pytest.raises(ValueError) as err:
        _ = list(chunker())
    assert 'supply either chunksize or memory_limit' in str(err)


@pytest.mark.parametrize('memory_limit_mb, expected', [
    (2, 524288),
    (100, 26214400),
])
def test_memory_limit(chunker, memory_limit_mb, expected):
    assert chunker._max_num_lightcurves(memory_limit_mb) == expected


def test_chunker_returns_indexes(chunker):
    chunk_size = 50
    _, s = next(chunker(chunksize=chunk_size))
    assert s == slice(0, 50, None)


'''
Expected API

with fitsio.FITS(filename) as infile:
    hdu = infile['flux']
    chunker = fitsioyielder.ChunkedAdapter(hdu)
    for chunk in chunker(chunksize=10): # or chunker(memory_limit=2048)
        # do something with chunk
'''
