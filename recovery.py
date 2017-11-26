#!/usr/bin/env python2
import os
import os.path
import sys
import jpgSorter, numberOfFilesPerFolderLimiter
import shutil
from time import localtime, strftime
import math
import multiprocessing as mp


def getNumberOfFilesInFolderRecursively(start_path = '.'):
    numberOfFiles = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if(os.path.isfile(fp)):
                numberOfFiles += 1
    return numberOfFiles


def getNumberOfFilesInFolder(path):
    return len(os.listdir(path))


def log(logString):
    print(strftime("%H:%M:%S", localtime()) + ": " + logString)


def moveFile(file, destination):
    extension = os.path.splitext(file)[1][1:].upper()
    sourcePath = os.path.join(root, file)

    destinationDirectory = os.path.join(destination, extension)

    if not os.path.exists(destinationDirectory):
        os.mkdir(destinationDirectory)

    fileName = str(fileCounter) + "." + extension.lower()
    destinationFile = os.path.join(destinationDirectory, fileName)
    if not os.path.exists(destinationFile):
        shutil.copy(sourcePath, destinationFile)


def get_args():
    import argparse

    description = (
        "Sort files recoverd by Photorec.\n"
        "The input files are first copied to the destination, sorted by file type.\n"
        "Then JPG files are sorted based on creation year (and optionally month).\n"
        "Finally any directories containing more than a maximum number of files are accordingly split into separate directories."
    )

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('source', metavar='src', type=str, help='source directory with files recovered by Photorec')
    parser.add_argument('destination', metavar='dest', type=str, help='destination directory to write sorted files to')
    parser.add_argument('-n', '--max-per-dir', type=int, default=500, required=False, help='maximum number of files per directory')
    parser.add_argument('-m', '--split-months', action='store_true', required=False, help='split JPEG files not only by year but by month as well')

    return parser.parse_args()



maxNumberOfFilesPerFolder = 500
splitMonths = False
source = None
destination = None


args = get_args()
source = args.source
destination = args.destination
maxNumberOfFilesPerFolder = args.max_per_dir
splitMonths = args.split_months

print("Reading from source '%s', writing to destination '%s' (max %i files per directory, splitting by year %s)." %
    (source, destination, maxNumberOfFilesPerFolder, splitMonths and "and month" or "only"))

while ((source is None) or (not os.path.exists(source))):
    source = input('Enter a valid source directory\n')
while ((destination is None) or (not os.path.exists(destination))):
    destination = input('Enter a valid destination directory\n')

fileNumber = getNumberOfFilesInFolderRecursively(source)
onePercentFiles = int(fileNumber/100)
totalAmountToCopy = str(fileNumber)
print("Files to copy: " + totalAmountToCopy)


fileCounter = 0
for root, dirs, files in os.walk(source, topdown=False):

    for file in files:
        extension = os.path.splitext(file)[1][1:].upper()
        sourcePath = os.path.join(root, file)

        destinationDirectory = os.path.join(destination, extension)

        if not os.path.exists(destinationDirectory):
            os.mkdir(destinationDirectory)

        fileName = str(fileCounter) + "." + extension.lower()
        destinationFile = os.path.join(destinationDirectory, fileName)
        if not os.path.exists(destinationFile):
            shutil.copy2(sourcePath, destinationFile)

        fileCounter += 1
        if((fileCounter % onePercentFiles) is 0):
            log(str(fileCounter) + " / " + totalAmountToCopy + " processed.")

log("start special file treatment")
jpgSorter.postprocessImages(os.path.join(destination, "JPG"), splitMonths)

log("assure max file per folder number")
numberOfFilesPerFolderLimiter.limitFilesPerFolder(destination, maxNumberOfFilesPerFolder)
