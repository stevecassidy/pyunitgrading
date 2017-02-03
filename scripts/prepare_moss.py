
from pyunitgrading.filehandling import unpack_submissions, gather_sourcefiles
import sys, os
import argparse


import zipfile


def prepare_moss(zipfile, outdir, targetfiles, expectzip):
    """Gather the target files together for each student in outdir
    """

    unpacked, problems = unpack_submissions(zipfile, outdir, targetfiles[0], expectzip)
    
    print("Unpacked %d submissions" % (len(unpacked),))
    if problems != []:
        for p in problems:
            print(p)
    
    for subdir in os.listdir(outdir):
        gather_sourcefiles(os.path.join(outdir, subdir), targetfiles)
    

def Parser():
  the_parser = argparse.ArgumentParser(description="unpack an iLearn zip file")  
  the_parser.add_argument('--expectzip', required=False, action="store_true", help="does the zip file contain more zip files")
  the_parser.add_argument('--out', required=False, default='moss_submission', 
                          help="name of the output directory, default 'moss_submission'")
  the_parser.add_argument('zipfile', action="store", type=str, help="downloaded zip file")
  the_parser.add_argument('file', nargs=argparse.REMAINDER, 
                          help="file name to be included in submission")
  args = the_parser.parse_args()
  return args

if __name__=='__main__':

    args = Parser()
    
    prepare_moss(args.zipfile, args.out, args.file, args.expectzip)
