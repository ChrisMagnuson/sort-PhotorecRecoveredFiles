import sys
import math
import os
import shutil


def limitFilesPerFolder(folder, maxNumberOfFilesPerFolder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir in dirs:
            dirPath = os.path.join(root, dir)
            filesInFolder = len(os.listdir(dirPath))
            if(filesInFolder > maxNumberOfFilesPerFolder):
                numberOfSubfolders = ((filesInFolder - 1) // maxNumberOfFilesPerFolder) + 1
                for subFolderNumber in range(1, numberOfSubfolders+1):
                    subFolderPath = os.path.join(dirPath, str(subFolderNumber))
                    if not os.path.exists(subFolderPath):
                        os.mkdir(subFolderPath)
                fileCounter = 1
                for file in os.listdir(dirPath):
                    source = os.path.join(dirPath, file)
                    if os.path.isfile(source):
                        destDir = str(((fileCounter - 1) // maxNumberOfFilesPerFolder) + 1)
                        destination = os.path.join(dirPath, destDir, file)
                        shutil.move(source, destination)
                        fileCounter += 1


