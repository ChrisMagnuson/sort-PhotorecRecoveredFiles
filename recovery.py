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



maxNumberOfFilesPerFolder = 500
source = None
destination = None

if(len(sys.argv) < 3):
	print("Enter source and destination: python sort.py source/path destination/path")
else:
	source = sys.argv[1]
	print("Source directory: " + source)
	destination = sys.argv[2]
	print("Destination directory: " + destination)

if(len(sys.argv) > 3):
	maxNumberOfFilesPerFolder = int(sys.argv[3])

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
jpgSorter.postprocessImages(os.path.join(destination, "JPG"), False)

log("assure max file per folder number")
numberOfFilesPerFolderLimiter.limitFilesPerFolder(destination, maxNumberOfFilesPerFolder)
