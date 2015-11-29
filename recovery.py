#!/usr/bin/env python2
import os
import os.path
import sys
import jpgSorter
import time
import shutil
from time import gmtime, strftime


def getFolderSizeInGb(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return int(total_size / 1024 / 1024 / 1024)


source = None
destination = None

if(len(sys.argv) < 3):
	print("Enter source and destination: python sort.py source/path destination/path")
else:
	source = sys.argv[1]
	print("Source directory: " + source)
	destination = sys.argv[2]
	print("Destination directory: " + destination)

while ((source is None) or (not os.path.exists(source))):
	source = input('Enter a valid source directory\n')
while ((destination is None) or (not os.path.exists(destination))):
	destination = input('Enter a valid destination directory\n')

totalAmountToCopy = str(getFolderSizeInGb(source))
print("Files to copy: " + totalAmountToCopy + " GB.")

images = []
for root, dirs, files in os.walk(source, topdown=False):
	print (strftime("%H:%M:%S", gmtime()) + ": " + str(getFolderSizeInGb(destination)) + " / " + totalAmountToCopy + " GB processed.")
	for file in files:
		extension = os.path.splitext(file)[1][1:].upper()
		path = os.path.join(root,file)
		
		destinationPath = os.path.join(destination, extension)

		if not os.path.exists(destinationPath):
			os.mkdir(destinationPath)
		
		if extension == "JPG":
			jpgSorter.postprocessImage(images, root, destinationPath, file)
		else:
			if os.path.exists(os.path.join(destinationPath, file)):
				shutil.copy(os.path.join(root,file), os.path.join(destination, extension, str(time.time()) + file))
			else:
				shutil.copy(os.path.join(root,file), destinationPath)

jpgSorter.writeImages(images, os.path.join(destination, "JPG"))
