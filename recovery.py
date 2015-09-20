#!/usr/bin/env python2
import os
import os.path
import shutil
import sys
import time
import exifread

source = sys.argv[1]
destination = sys.argv[2]

minEventDelta = 60 * 60 * 24 * 4 # 4 days in seconds


def getMinimumCreationTime(exif_data):
    creationTime = None
    dateTime = exif_data.get('DateTime')
    dateTimeOriginal = exif_data.get('EXIF DateTimeOriginal')
    dateTimeDigitized = exif_data.get('EXIF DateTimeDigitized')
    
    if dateTime is not None :
        creationTime = dateTime
    if dateTimeOriginal is not None and (creationTime == None or dateTimeOriginal < creationTime):
        creationTime = dateTimeOriginal
    if dateTimeDigitized is not None and (creationTime == None or dateTimeDigitized < creationTime):
        creationTime = dateTimeDigitized
    return creationTime

def postprocessImage(images, sourceDir, imageDirectory, fileName):
    imagePath = os.path.join(sourceDir, fileName)
    image = open(imagePath, 'rb')
    exifTags = exifread.process_file(image)
    creationTime = getMinimumCreationTime(exifTags)

    # distinct different time types
    if creationTime is None:
        creationTime = time.gmtime(os.path.getctime(imagePath))
    else:
        creationTime = time.strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")
        
    print time.asctime(creationTime)

    images.append((time.mktime(creationTime), imagePath))


def createNewFolder(destinationRoot, year, eventNumber):
    yearPath = os.path.join(destinationRoot, year)
    if not os.path.exists(yearPath):
        os.mkdir(yearPath)
    eventPath = os.path.join(yearPath, str(eventNumber))
    if not os.path.exists(eventPath):
        os.mkdir(eventPath)


def writeImages(images, destinationRoot):
    sortedImages = sorted(images)
    previousTime = None
    eventNumber = 0

    for imageTuple in sortedImages:
        t = time.gmtime(imageTuple[0])
        year = time.strftime("%Y", t)
        if (previousTime == None) or ((previousTime + minEventDelta) < imageTuple[0]):
            previousTime = imageTuple[0]
            eventNumber = eventNumber + 1
            createNewFolder(destinationRoot, year, eventNumber)
        
        previousTime = imageTuple[0]

        destination = os.path.join(destinationRoot, year, str(eventNumber))
        shutil.copy(imageTuple[1], destination)


images = []
while not os.path.exists(source):
    source = raw_input('Enter a valid source directory\n')
while not os.path.exists(destination):
    destination = raw_input('Enter a valid destination directory\n')

for root, dirs, files in os.walk(source, topdown=False):
    for file in files:
        extension = os.path.splitext(file)[1][1:].upper()
        path = os.path.join(root,file)
        
        destinationPath = os.path.join(destination, extension)

        if not os.path.exists(destinationPath):
            os.mkdir(destinationPath)
        
        if extension == "JPG":
            postprocessImage(root, destinationPath, file)
        else:
            if os.path.exists(os.path.join(destinationPath,file)):
                print("WARNING: this file was not copied :" + os.path.join(root,file))
                shutil.copy(os.path.join(root,file), os.path.join(destination, extension, str(time.time()) + file))
            else:
                shutil.copy(os.path.join(root,file), destinationPath)

writeImages(os.path.join(destination, "JPG"))