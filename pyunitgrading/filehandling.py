"""
Code for unpacking zip files from iLearn
"""

import zipfile
import re
import os, shutil

UNRAR = '/usr/local/bin/unrar'
TAR = '/usr/bin/tar'
SEVENZ = '/usr/local/bin/7z'

def parse_submission_name(fname):
    """Extract the student identifying info
    from the submission name, return a tuple
    (id, pid) where
     id - the student id
     pid - the student Participant ID (unique id for this submission)

     The pid cross references to the grading spreadsheet downloadable from iLearn"""


    # eg 42873711_10413_assignsubmission_file_workshop1.py
    #    43696864_5132128_assignsubmission_file_43696864_GPSTracks.zip

    pattern = r'([^_]+)_([0-9]+)_.*'

    match = re.match(pattern, fname)
    if match:
        sid = match.group(1)
        pid = match.group(2)
        return (sid, pid)
    else:
        raise Exception("Can't parse identifier in name %s" % fname)


def unpack_submissions(zfile, targetdir, targetname=None, expectzip=False):
    """Given a zip file, unpack the submissions into a
    target directory with one directory per student named
    for their studentid
    rename the submitted file to targetname if supplied unless it's a zip file
    return a tuple of two lists (unpacked, problems)
    where unpacked is a list of student ids that were ok
    and problems are student ids that are not ok
    """

    zf = zipfile.ZipFile(zfile)
    names = zf.namelist()

    unpacked = []
    problems = []
    for name in names:
        # names are like:
        #   42873711_10413_assignsubmission_file_workshop1.py
        #
        (sid, pid) = parse_submission_name(name)
        sdir = os.path.join(targetdir, sid)
        if not os.path.exists(sdir):
            os.makedirs(sdir)
        extracted = os.path.abspath(zf.extract(name, sdir))
        # check if this is a zip file
        if expectzip:
            if is_archive(extracted):
                unpack_one(extracted, sdir)
            else:
                problems.append("Not an archive file I recognise: " + extracted)
            unpacked.append(sid)
        elif targetname != None:
            # rename file to target name
            os.rename(extracted, os.path.join(sdir, targetname))
            unpacked.append(sid)
        else:
            # we do nothing
            unpacked.append(sid)

    return (unpacked, problems)






def is_archive(filename):
    """Test to see whether this is an archive file (zip, rar, tgz),
     return True if it is, False if not"""

    (base, ext) = os.path.splitext(filename)
    return ext in ['.zip', '.rar', '.tgz', '.7z']



def unpack_one(subfile, sdir):
    """Unpack a single file submitted by a student that might be
     a zipfile but could also be a tar or rar file (or none of these)"""

    problem = ""
    (base, ext) = os.path.splitext(subfile)
    if ext == '.zip':
        if not unzip(subfile, sdir):
            problem = "Unable to unzip file " + subfile
    elif ext == '.rar':
        if not unrar(subfile, sdir):
            problem = "Unable to unpack RAR file " + subfile
    elif ext == '.tgz':
        if not untar(subfile, sdir):
            problem = "Unable to unpack tar file " + subfile
    elif ext == '.7z':
        if not un7z(subfile, sdir):
            problem = "Unable to unpack tar file " + subfile
    else:
        status = False
        problem = "Unknown file extension: " + subfile

    if problem != "":
        h = open('unpack_problems.txt', 'w')
        h.write(sdir + ": " + problem)
        h.close()

        print(problem)
    else:
        # remove the archive if there were no problems
        os.unlink(subfile)


def unzip(zfile, outdir):
    """Unpack a zip file into the given output directory outdir
    Return True if it worked, False otherwise"""

    try:
        zf2 = zipfile.ZipFile(zfile)
        zf2.extractall(outdir)
        return True
    except zipfile.BadZipfile:
        return False
    except NotImplementedError:
        return False


from subprocess import call

def unrar(rarfile, outdir):
    """Unpack a RAR file into the target directory outdir
    Return True if it worked, False otherwise"""

    cmd = [UNRAR, "x", "-idcdpq", "-y", rarfile]

    cwd = os.getcwd()
    os.chdir(outdir)
    retcode = call(cmd)
    os.chdir(cwd)

    return retcode >= 0

def untar(tarfile, outdir):
    """Unpack a tar file into the target directory outdir
    Return True if it worked, False otherwise"""

    cmd = [TAR, "xzf", tarfile]

    cwd = os.getcwd()
    os.chdir(outdir)
    retcode = call(cmd)
    os.chdir(cwd)

    return retcode >= 0


def un7z(file, outdir):
    """Unpack a 7z file into the target directory outdir
    Return True if it worked, False otherwise"""

    cmd = [SEVENZ, "x", "-y", file]

    cwd = os.getcwd()
    os.chdir(outdir)
    retcode = call(cmd)
    os.chdir(cwd)

    return retcode >= 0


def isolate_directory(topdir, target, containing=None):
    """Find the directory named 'target' underneath 'topdir'
    and make it the top level directory inside topdir.
    If containing is not None, the target directory should contain a file
    with this name.
    Use for finding a package directory inside an eclipse export
    and making it the top level directory."""

    subdirs = os.listdir(topdir)
    for (dirpath, dirnames, filenames) in os.walk(topdir):
        for dirname in dirnames:
            if dirname == target:
                contained = os.listdir(os.path.join(dirpath, dirname))
                if containing != None and containing in contained:
                    try:
                        os.rename(os.path.join(dirpath, dirname), os.path.join(topdir, dirname))

                        # remove the original top level directories and files
                        for d in subdirs:
                            path = os.path.join(topdir, d)
                            if os.path.isdir(path):
                                shutil.rmtree(path)
                            else:
                                os.unlink(path)

                        return
                    except:
                        print("Problem isolating in ", dirpath)


def gather_sourcefiles(topdir, targetfiles):
    """Find the target files underneath topdir and move them into topdir,
    remove everything else in topdir
    targetfiles - a list of filenames"""

    original = os.listdir(topdir)
    for (dirpath, dirnames, filenames) in os.walk(topdir):
        for filename in filenames:
            if filename in targetfiles:
                os.rename(os.path.join(dirpath, filename), os.path.join(topdir, filename))

    # remove the original top level directories and files
    for d in original:
        path = os.path.join(topdir, d)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif not os.path.basename(path) in targetfiles:
            os.unlink(path)
