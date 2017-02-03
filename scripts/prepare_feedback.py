
from pyunitgrading.filehandling import parse_submission_name
import sys, os
import argparse
from glob import glob

import zipfile

def gather_feedback(zfile, targetdir, targetname, outname):

    zf = zipfile.ZipFile(zfile)
    names = zf.namelist()

    fd = open(outname, 'wb')
    outzf = zipfile.ZipFile(fd, mode='w')

    unpacked = []
    problems = []
    for name in names:
        # names are like:
        #   42873711_10413_assignsubmission_file_workshop1.py
        #
        (sid, pid) = parse_submission_name(name)
        sdir = os.path.join(targetdir, sid)

        targetfile = os.path.join(sdir, targetname)

        for filename in glob(targetfile):
            newname = sid + "_" + pid + "_assignsubmission_file_" + os.path.basename(filename)
            print(filename, newname)
            outzf.write(filename, arcname=newname)



def Parser():
  the_parser = argparse.ArgumentParser(description="gather feedback files after running tests and prepare for upload to iLearn")
  the_parser.add_argument('--targetname', required=False, default='test_output.txt', type=str, help="name (or glob pattern) of feedback file to look for, default test_output*.txt")
  the_parser.add_argument('zipfile', action="store", type=str, help="downloaded zip file")
  the_parser.add_argument('targetdir', help="directory with unpacked files")
  the_parser.add_argument('output', help="name of the output zip file")
  args = the_parser.parse_args()
  return args

if __name__=='__main__':

    args = Parser()

    gather_feedback(args.zipfile, args.targetdir, args.targetname, args.output)
