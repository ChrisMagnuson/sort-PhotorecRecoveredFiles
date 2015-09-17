#!/usr/bin/env python2
import os
import os.path
import shutil
import sys
import time
import exifread

source = sys.argv[1]
destination = sys.argv[2]


def get_minimum_creation_time(exif_data):
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

def postprocess_image(sourceDir, imageDirectory, fileName):
    imagePath = os.path.join(sourceDir, fileName)
    image = open(imagePath, 'rb')
    exifTags = exifread.process_file(image)
    creationTime = get_minimum_creation_time(exifTags)

    # distinct different time types
    if creationTime is None:
        creationTime = time.gmtime(os.path.getctime(imagePath))
    else:
        creationTime = time.strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")
        
    print time.asctime(creationTime)

    year = time.strftime("%Y", creationTime)
    month = time.strftime("%m")

    yearPath = os.path.join(imageDirectory, year)

    if not os.path.exists(yearPath):
        os.mkdir(yearPath)

    monthPath = os.path.join(yearPath, month)

    if not os.path.exists(monthPath):
        os.mkdir(monthPath)

    shutil.copy(imagePath, os.path.join(monthPath, file))


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
            postprocess_image(root, destinationPath, file)
            print "sorted jpg"
        else:
            if os.path.exists(os.path.join(destinationPath,file)):
                print("WARNING: this file was not copied :" + os.path.join(root,file))
                shutil.copy(os.path.join(root,file), os.path.join(destination, extension, str(time.time()) + file))
            else:
                shutil.copy(os.path.join(root,file), destinationPath)