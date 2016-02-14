fitsiochunked
=============

![image](https://img.shields.io/travis/mindriot101/fitsiochunked.svg)(https://travis-ci.org/mindriot101/fitsiochunked)

Package to efficiently read large fits arrays in object by object

- Free software: MIT license

Features
--------

- Read in large fits files, within a given fixed memory limit

Quick usage
-----------

The following example shows an example of reading in a large fits hdu
within a memory limit of 2048MB, assuming light curves are stored in
rows:

```python
import numpy as np
import fitsio
from fitsiochunked import ChunkedAdapter

with fitsio.FITS(filename) as infile:
    hdu = infile['flux']
    napertures = hdu.get_info()['ndim'][0]
    mean_flux = np.zeros(napertures)

    chunker = ChunkedAdapter(hdu)
    for chunk in chunker(memory_limit_mb=2048):

        # `chunk` is a namedtuple with `.data` and `.slice` properties
        chunk_data = chunk.data
        print('Data shape:', chunk_data.shape)
        print('Data dtype:', chunk_data.dtype)


        chunk_slice = chunk.slice
        print('Chunk starting from aperture:', chunk_slice.start)
        print('Chunk up to:', chunk_slice.stop)

        chunk_mean = np.average(chunk_data, axis=1)
        mean_flux[chunk_slice] = chunk_mean
```

Details
-------

The main class created is the `ChunkedAdapter` adapter, which wraps a
`fitsio` HDU object. When constructed, it becomes a callable which
yields the image data in that hdu in chunks.

The chunksize can be set either with with the parameter `chunksize`
which simply yields `chunksize` rows each time, or with
`memory_limit_mb` which *tries* (no promises!) to automatically
calculate the number of lightcurves that will fit into `memory_limit_mb`
megabytes of memory.
