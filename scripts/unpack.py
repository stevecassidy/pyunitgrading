
from pyunitgrading import unpack_submissions
import sys
import argparse

def Parser():
  the_parser = argparse.ArgumentParser(description="unpack an iLearn zip file")
  the_parser.add_argument('--expectzip', required=False, action="store_true", help="does the zip file contain more zip files")
  the_parser.add_argument('--targetname', required=False, type=str, help="name for student submission files")
  the_parser.add_argument('zipfile', action="store", type=str, help="downloaded zip file")
  the_parser.add_argument('csvfile', action="store", type=str, help="csv grading spreadsheet from iLearn")
  the_parser.add_argument('targetdir', help="directory to store unpacked files")
  args = the_parser.parse_args()
  return args

if __name__=='__main__':

    args = Parser()
        
    unpacked, problems = unpack_submissions(args.zipfile, args.csvfile, args.targetdir, args.targetname, args.expectzip)
    
    print("Unpacked %d submissions" % (len(unpacked),))
    if problems != []:
        for p in problems:
            print(p)