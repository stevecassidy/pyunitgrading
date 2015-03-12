#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyunitgrading
----------------------------------

Tests for `pyunitgrading` module.
"""

import unittest
import shutil

from pyunitgrading import *
import os

TESTDIR = os.path.dirname(__file__)

class TestPyunitgrading(unittest.TestCase):

    def setUp(self):
        pass

    def test_unpack(self):
        
        zfile = os.path.join(TESTDIR, 'ziptest.zip')
        outdir = os.path.join(TESTDIR, 'tmp')
        self.addCleanup(lambda: shutil.rmtree(outdir))
        
        expected = ['42427932', '42444314', '42447321', '42461715', '42469872', '42482402', '42863066', '42938732']
        
        unpacked, problems = unpack_submissions(zfile, outdir, expectzip=True)

        self.assertEqual(expected, unpacked)
        self.assertEqual([], problems)
        
    
    def test_runtests(self):
        
        zfile = os.path.join(TESTDIR, 'workshop1', 'COMP249_FHFYR_2013_ALL_U-Workshop Task 1 Submission-Monday 4-6 Ian-1688117.zip')
        configfile = os.path.join(TESTDIR, 'workshop1', 'config.ini')
        
        process(zfile, configfile)
        
        
        


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
