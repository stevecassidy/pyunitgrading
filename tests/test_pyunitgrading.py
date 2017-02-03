#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyunitgrading
----------------------------------

Tests for `pyunitgrading` module.
"""

import unittest
import shutil

import pyunitgrading

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
        
        unpacked, problems = pyunitgrading.unpack_submissions(zfile, outdir, expectzip=True)

        self.assertEqual(expected, unpacked)
        self.assertEqual([], problems)
        
    
    #def test_runtests(self):
        
    #    zfile = os.path.join(TESTDIR, 'workshop1', 'COMP249_FHFYR_2013_ALL_U-Workshop Task 1 Submission-Monday 4-6 Ian-1688117.zip')
    #    configfile = os.path.join(TESTDIR, 'workshop1', 'config.ini')
        
    #    process(zfile, configfile)
        
        
    def test_runtests2(self):
        
        zfile = os.path.join(TESTDIR, 'bad', 'single-sub.zip')
        configfile = os.path.join(TESTDIR, 'bad', 'single.ini')
        
        #dirlist = ['43684882', '42488869', '43555195', '41749952']
        dirlist = ['43555195', '41749952']
        basedir = "tests/bad/single"
        testmodule = "alltests"
        targetname = "main.py"
        modules = [os.path.join(TESTDIR, "bad", "alltests.py")]
        outputname = "test_output.txt"

        result = pyunitgrading.testrunner.run_tests_on_collection(dirlist, basedir, testmodule, targetname, modules, outputname)
        
        for row in result:
            print(row)
        
        
    


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
