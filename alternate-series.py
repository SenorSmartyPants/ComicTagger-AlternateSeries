#!/usr/bin/python
import sys
#using LSIO docker paths

#something is weird with the path. Not finding the libs but this path is at the end of the path list
#insert into the start of path and then script works
sys.path.insert(0,'/app/mylar/lib')

from comictaggerlib.settings import *
from comictaggerlib.comicarchive import *

from titleparsing import *

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

    #image path needed to start ComicArchive, not sure why.
    #default image path is null in settings
    ca = ComicArchive(
        filename,
        settings.rar_exe_path,
        ComicTaggerSettings.getGraphic('nocover.png'))

    if not ca.seemsToBeAComicArchive():
        print >> sys.stderr, "Sorry, but " + \
            filename + " is not a comic archive!"
        return

    style = MetaDataStyle.CIX #ComicRack Style metadata

    if ca.hasMetadata( style ):
        md = ca.readMetadata( style )
        print "{0} #{1} ({2})".format(md.series, md.issue, md.year)

        print "Title={0}".format(md.title)
        print "SA={0}".format(md.storyArc)
        print "AS={0} #{1}".format(md.alternateSeries, md.alternateNumber)

        #move story arc to Alternate series
        #then process for numbers
        if md.alternateSeries is None:
            #don't overwrite non empty alternate series
            md.alternateSeries = md.storyArc
            md.storyArc = None

        if md.title is not None or md.alternateSeries is not None:
            SingleStoryArcFromTitle(md)

            if md.alternateNumber is None:
                print "no alternate Number found"

            print "---After Modifications---"
            print "SA={0}".format(md.storyArc)
            print "AS={0} #{1}".format(md.alternateSeries, md.alternateNumber)

            if not ca.writeMetadata(md, style):
                print >> sys.stderr, "The tag save seemed to fail!"
                return False
            else:
                print >> sys.stderr, "Save complete."


if __name__ == '__main__':
    main()