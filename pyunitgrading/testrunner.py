"""
  run unit tests for a set of student submissions downloaded from iLearn (moodle)

"""

import unittest
import os
import traceback
import sys
import importlib
import imp
import threading
import zipfile
import re
import shutil
import csv
import configparser
import subprocess

from pyunitgrading.filehandling import unpack_submissions


def report_error(pid, message):
    """Report an error for this student"""
    
    out = os.path.join(pid, "test_errors.txt")
    ostream = open(out,"a")
    
    print("\tError running tests:", message)
    ostream.write("Error running tests\n")
    ostream.write(message + "\n")




def find_sourcedir(basedir, modulename):
    """Locate the sourcedir by looking for the modulename
    to be tested inside a subfolder of basedir"""
    
    for dirpath, dirnames, filenames in os.walk(basedir):
        if modulename in filenames:
            return dirpath
    
    # if we don't find it, raise an error
    report_error(basedir, "Can't locate module %s" % modulename)
    
    return basedir



class TestRunnerThread(threading.Thread):
    """Class to run a set of unit tests in a separate thread"""


    def __init__(self, basedir, sid, testmodulename, targetname, modules, outputname):
        """Initialise a test runner
          basedir - directory in which student submissions are unpacked
          sid - student id
          testmodulename - name of the test module to run
          targetname - name of a source module in the submission
          modules - list of python modules to be copied into project, including test module
        """
        threading.Thread.__init__(self)
        self.sid = sid
        self.modules = modules
        self.testmodulename = testmodulename
        self.targetname = targetname
        self.result = (self.sid, 0, 0, 0, 0)
        self.rootdir = os.getcwd()
        
        out = os.path.join(basedir, sid, outputname)
        self.ostream = open(out,"w")
        
        self.sourcedir = find_sourcedir(os.path.join(basedir, sid), self.targetname)

    def __report_error(self, message=""):
        """Report an error, either an explicit message
        or just dump out crash info"""
        
        print("\tError running test")
        self.ostream.write("Error running tests\n")
        if message != "":
            self.ostream.write(message + "\n")
            print(message)
        else:
            info = sys.exc_info()
            self.ostream.write(str(info))
            traceback.print_exc(None, self.ostream)


    def run(self):
        print("DIR", self.sourcedir)
        
        # get the python script to test from the given directory: add it to the path
        sys.path.insert(0, '.')
        
        # any modules already in this dir should be reloaded
        reloadmods = []
        for modfile in os.listdir(self.sourcedir):
            if modfile.endswith('.py'):
                modname, ext = os.path.splitext(modfile)
                reloadmods.append(modname)
        
        # copy the test module file into the target dir
        for m in self.modules:
            shutil.copy(m, self.sourcedir)

        try:
            os.chdir(self.sourcedir)
            
            # reload any user modules
            for modname in reloadmods:
                if modname in sys.modules:
                    #print('\treloading', sys.modules[modname])
                    target = imp.reload(sys.modules[modname])
            
            testmodule = importlib.import_module(self.testmodulename)
            # load all tests in the module 
            suite = unittest.defaultTestLoader.loadTestsFromModule(testmodule)
            # run the tests
            result = unittest.TextTestRunner(stream=self.ostream, verbosity=2).run(suite)
            
            totalmark = result.testsRun-len(result.errors)-len(result.failures)

            self.result = (self.sid, result.testsRun, len(result.failures), len(result.errors), totalmark)
            
        except:
            self.__report_error()
            
        finally:
            # ensure we reset the path
            sys.path.pop(0)
            os.chdir(self.rootdir)
            self.ostream.close()


def read_config(configfile):
    """Read config file and set up defaults,
    return a dictionary of config values"""
    
    r = dict()
    config = configparser.SafeConfigParser()
    config.read(configfile)

    r['basedir'] = config.get('default', 'basedir')
    r['targetname'] = config.get('default', 'targetname', fallback=None)
    r['testmodule'] = config.get('default', 'testmodule')
    r['outputname'] = config.get('default', 'outputname',  fallback='test_output.txt')
 
    expectzip = config.get('default', 'expectzip', fallback='no')
    r['expectzip'] = expectzip == 'yes'
    
    modules = config.get('default', 'modules')
    # we split modules on whitespace
    r['modules'] = modules.split()

    r['csvname'] = config.get('default', 'csvname', fallback="results.csv")
    
    return r
    

def process(zfile, configfile):
    """Unpack submissions and run the unit tests for each
    student"""

    c = read_config(configfile)
    
    h = open(c['csvname'], 'w')
    results = csv.writer(h)

    results.writerow(('SID', 'Tests', 'Failed', 'Errors', 'Total'))

    unpacked, problems = unpack_submissions(zfile, c['basedir'], c['targetname'], c['expectzip'])

    for sid in unpacked:
        thr = TestRunnerThread(c['basedir'], sid, c['testmodule'], c['targetname'], c['modules'], c['outputname'])
        thr.start()
        while thr.is_alive():
            pass
        sid, testsRun, failures, errors, total = thr.result

        results.writerow((sid, testsRun, failures, errors, total))
        

    print("Problem cases:\n")
    for sid in problems:
        results.writerow((sid,))
        print(sid)

    h.close()

    print("Grading complete")
    print("Results in ", c['csvname'])




