#!/usr/bin/python3
import sys
from comictagger_utils import *
from titleparsing import *

def main():
    print(__name__)
    filename = getFilename()
    ca = getComicArchive(filename)
    style = MetaDataStyle.CIX #ComicRack Style metadata

    if ca.hasMetadata( style ):
        md = ca.readMetadata( style )
        print("{0} #{1} ({2})".format(md.series, md.issue, md.year))

        print("Title={0}".format(md.title))
        print("SA={0}".format(md.storyArc))
        print("AS={0} #{1}".format(md.alternateSeries, md.alternateNumber))

        #move story arc to Alternate series
        #then process for numbers
        if md.alternateSeries is None:
            #don't overwrite non empty alternate series
            md.alternateSeries = md.storyArc
            md.storyArc = None

        if md.title is not None or md.alternateSeries is not None:
            SingleStoryArcFromTitle(md)

            if md.alternateNumber is None:
                print("no alternate Number found")

            print("---After Modifications---")
            print("SA={0}".format(md.storyArc))
            print("AS={0} #{1}".format(md.alternateSeries, md.alternateNumber))

            writeMetadata(md, ca, style)
    else:
        print("Comic archive does not have metadata", file=sys.stderr)

def SingleStoryArcFromTitle(metadata, overwrite = False):
	config.LoadSettings()
	books = []
	books.append(metadata)
	MultipleStoryArcsFromTitles(books,0)
#end SingleStoryArcFromTitle

def MultipleStoryArcsFromTitles(books,method_selected):
	titleArray = makeTitleArray(books)
	storyarcs = prefix_groups(titleArray,method_selected)

	if storyarcs:
		#invert dictionary, so book title is now the key, story arc the value
		inv = InvertDictionary(storyarcs)
		updateBooksAlternateSeries(books, inv, False)

#end MultipleStoryArcsFromTitles

if __name__ == '__main__':
    main()