import sys

#using LSIO docker paths
#something is weird with the path. Not finding the libs but this path is at the end of the path list
#insert into the start of path and then script works
sys.path.insert(0,'/app/mylar3/lib/')

from comictaggerlib.settings import *
from comictaggerlib.comicarchive import *

def getFilename():
    if len(sys.argv) < 2:
        print("Usage: {0} [comicfile]".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print(filename + ": not found!", file=sys.stderr)
        sys.exit(1)

    return filename

def getFilenames():
    if len(sys.argv) < 2:
        print("Usage: {0} [comicfile]".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    filenames = sys.argv[1:]

    return filenames

def getComicArchive(filename):
    settings = ComicTaggerSettings('/config/.ComicTagger')

    if not os.path.exists(filename):
        print(filename + ": not found!", file=sys.stderr)
        return None

    #image path needed to start ComicArchive, not sure why.
    #default image path is null in settings
    ca = ComicArchive(
        filename,
        settings.rar_exe_path,
        ComicTaggerSettings.getGraphic('nocover.png'))

    if not ca.seemsToBeAComicArchive():
        print("Sorry, but " + \
            filename + " is not a comic archive!", file=sys.stderr)
        return None

    return ca

def writeMetadata(md, ca, style):
    #save metadata
    if not ca.writeMetadata(md, style):
        print("The tag save seemed to fail!", file=sys.stderr)
        return False
    else:
        print("Save complete.", file=sys.stderr)