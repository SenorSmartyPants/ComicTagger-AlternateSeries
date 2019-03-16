#!/usr/bin/python
import sys
#using LSIO docker paths

#something is weird with the path. Not finding the libs but this path is at the end of the path list
#insert into the start of path and then script works
sys.path.insert(0,'/app/mylar/lib')

from comictaggerlib.settings import *
from comictaggerlib.comicarchive import *


def main():

    utils.fix_output_encoding()
    settings = ComicTaggerSettings()

    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: {0} [comicfile]".format(
            sys.argv[0])
        return

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print >> sys.stderr, filename + ": not found!"
        return

    ca = ComicArchive(filename, settings)
    if not ca.seemsToBeAComicArchive():
        print >> sys.stderr, "Sorry, but " + \
            filename + " is not a comic archive!"
        return

    if ca.hasMetadata( style ):
        md = ca.readMetadata( style )
        print "{0} #{1} ({2})".format(md.series, md.issue, md.year)


if __name__ == '__main__':
    main()