import os.path
import exifread
import time
import shutil

minEventDelta = 60 * 60 * 24 * 4 # 4 days in seconds

def getMinimumCreationTime(exif_data):
    creationTime = None
    dateTime = exif_data.get('DateTime')
    dateTimeOriginal = exif_data.get('EXIF DateTimeOriginal')
    dateTimeDigitized = exif_data.get('EXIF DateTimeDigitized')

    # 3 differnt time fields that can be set independently result in 9 if-cases
    if (dateTime is None):
        if (dateTimeOriginal is None):
            # case 1/9: dateTime, dateTimeOriginal, and dateTimeDigitized = None
            # case 2/9: dateTime and dateTimeOriginal = None, then use dateTimeDigitized
            creationTime = dateTimeDigitized 
        else:
            # case 3/9: dateTime and dateTimeDigitized = None, then use dateTimeOriginal
            # case 4/9: dateTime = None, prefere dateTimeOriginal over dateTimeDigitized
            creationTime = dateTimeOriginal
    else:
        # case 5-9: when creationTime is set, prefere it over the others
        creationTime = dateTime

    return creationTime

def postprocessImage(images, sourceDir, imageDirectory, fileName):
    imagePath = os.path.join(sourceDir, fileName)
    image = open(imagePath, 'rb')
    try: 
        exifTags = exifread.process_file(image, details=False)
    except:
        print("invalid exif tags for " + fileName)
    creationTime = getMinimumCreationTime(exifTags)

    # distinct different time types
    if creationTime is None:
        creationTime = time.gmtime(os.path.getctime(imagePath))
    else:
        creationTime = time.strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")

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
