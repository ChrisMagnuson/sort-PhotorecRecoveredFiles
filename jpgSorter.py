import os.path
import ntpath
from time import localtime, strftime, strptime, mktime
import shutil
import exifread

unknownDateFolderName = "date-unknown"

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

def postprocessImage(images, imageDirectory, fileName):
    imagePath = os.path.join(imageDirectory, fileName)
    image = open(imagePath, 'rb')
    creationTime = None
    try:
        exifTags = exifread.process_file(image, details=False)
        creationTime = getMinimumCreationTime(exifTags)
    except:
        print("invalid exif tags for " + fileName)

    # distinct different time types
    if creationTime is None:
        creationTime = localtime(os.path.getctime(imagePath))
    else:
        try:
            creationTime = strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")
        except:
            creationTime = localtime(os.path.getctime(imagePath))

    images.append((mktime(creationTime), imagePath))
    image.close()

# Creates the requested path recursively.
def createPath(newPath):
    if not os.path.exists(newPath):
        os.makedirs(newPath)

# Pass None for month to create 'year/eventNumber' directories instead of 'year/month/eventNumber'.
def createNewFolder(destinationRoot, year, month, eventNumber):
    if month is not None:
        newPath = os.path.join(destinationRoot, year, month, str(eventNumber))
    else:
        newPath = os.path.join(destinationRoot, year, str(eventNumber))

    createPath(newPath)

def createUnknownDateFolder(destinationRoot):
    path = os.path.join(destinationRoot, unknownDateFolderName)
    createPath(path)

def writeImages(images, destinationRoot, minEventDeltaDays, splitByMonth=False):
    minEventDelta = minEventDeltaDays * 60 * 60 * 24 # convert in seconds
    sortedImages = sorted(images)
    previousTime = None
    eventNumber = 0
    previousDestination = None
    today = strftime("%d/%m/%Y")

    for imageTuple in sortedImages:
        destination = ""
        destinationFilePath = ""
        t = localtime(imageTuple[0])
        year = strftime("%Y", t)
        month = splitByMonth and strftime("%m", t) or None
        creationDate = strftime("%d/%m/%Y", t)
        fileName = ntpath.basename(imageTuple[1])

        if(creationDate == today):
            createUnknownDateFolder(destinationRoot)
            destination = os.path.join(destinationRoot, unknownDateFolderName)
            destinationFilePath = os.path.join(destination, fileName)

        else:
            if (previousTime == None) or ((previousTime + minEventDelta) < imageTuple[0]):
                eventNumber = eventNumber + 1
                createNewFolder(destinationRoot, year, month, eventNumber)

            previousTime = imageTuple[0]

            destComponents = [destinationRoot, year, month, str(eventNumber)]
            destComponents = [v for v in destComponents if v is not None]
            destination = os.path.join(*destComponents)

            # it may be possible that an event covers 2 years.
            # in such a case put all the images to the event in the old year
            if not (os.path.exists(destination)):
                destination = previousDestination
                # destination = os.path.join(destinationRoot, str(int(year) - 1), str(eventNumber))

            previousDestination = destination
            destinationFilePath = os.path.join(destination, fileName)

        if not (os.path.exists(destinationFilePath)):
            shutil.move(imageTuple[1], destination)
        else:
            if (os.path.exists(imageTuple[1])):
                os.remove(imageTuple[1])


def postprocessImages(imageDirectory, minEventDeltaDays, splitByMonth):
    images = []
    for root, dirs, files in os.walk(imageDirectory):
        for file in files:
            postprocessImage(images, imageDirectory, file)

    writeImages(images, imageDirectory, minEventDeltaDays, splitByMonth)
