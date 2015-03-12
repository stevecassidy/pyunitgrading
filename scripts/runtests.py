
from pyunitgrading import process
import sys

if __name__=='__main__':

    if len(sys.argv) != 3:
        print("Usage: runtests.py <iLearn Zip file> <config file>")
        exit
    else:
        zfile = sys.argv[1]
        configfile = sys.argv[2]

        process(zfile, configfile)
