===============================
PyUnit Grading
===============================

PyUnit Grading contains code to auto-mark programming assignments using Unit tests.  Write
unit tests to match the requirements you give to students (we generally give these
to students too).  These scripts run the unit tests over the student submissions and collate
the results in terms of tests passed etc.  They also deal with failing and crashing scripts. 

The code here is designed to work with submissions downloaded from the Macquarie instance of Moodle (iLearn) which are zip files with each entry named using a combination of the student ID and the
submitted file name.  Submissions can be single files or zip files. The code can unpack these
recursively and also unpack other archives (tgz, rar) if the tools are available on the local 
machine.  

The package installs two scripts: unpack.py and runtests.py.

unpack.py
=========

Unpacks a submitted zip file downloaded from Moodle (iLearn), possibly unpacking the archive files it contains. Generates a directory with one sub-directory per student named for their student ID. 

If the zip file contains single file submissions the files are renamed to a given file name within the student's sub-directory.

If the zip file contains archive files they are unpacked within the student's sub-directory if possible. If this fails, the archive is copied to the sub-directory and a warning is printed. 

Usage:

    usage: unpack.py [-h] [--expectzip EXPECTZIP] [--targetname TARGETNAME] zipfile targetdir

    positional arguments:
      zipfile               downloaded zip file
      targetdir             directory to store unpacked files

    optional arguments:
      -h, --help            show this help message and exit
      --expectzip           does the zip file contain more zip files
      --targetname TARGETNAME
                            name for student submission files

runtests.py
===========

Runs a test file for each submission in a zip file.

    Usage: runtests.py <iLearn Zip file> <config file>"


The config file is INI format file containing settings for the test run as follows:

    [default]

    basedir: tmp
    targetname: workshop1.py
    testmodule: workshop1test
    modules: workshop1test.py
    expectzip: True
    csvname: results.csv
    

* basedir is the directory that submissions will be unpacked to
* targetname is the name that each submission file is rename to in the student sub-directory, or, if the submissions are zip files, the name of one of the expected student source files (needed to find the submission in the zip file)
* testmodule the name of the python module containing unit tests (without the '.py' extension)
* modules a list of files to be copied into each student sub-directory before tests are run, this will probably include the test file and any required data files
* expectzip should be True if the submissions are zip files that need to be unpacked
* csvname the name of the csv file to write the summary results to


The tests will be run for each student submission. If there are errors in running the tests a message will be printed. Any output from the tests is stored in the student sub-directory in a file test_output.txt.   Any errors generated will be written to test_errors.txt.  











* Free software: BSD license
* Documentation: https://pyunitgrading.readthedocs.org.

Features
--------

* TODO
