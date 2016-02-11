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


