# Sort files recovered by Photorec

Photorec does a great job when recovering deleted files, but the result is a huge, unsorted, unnamed amount of files. Particularly for external hard drives that serve as a backup of all your personal data, sorting them is a tedious job.

This program helps you sort the files that Photorec recovers. First, the **files are sorted into folders by their file extensions**. Second, **JPGs** are then further sorted **by the year they were taken* and **by the event as part of which they were taken**. An event is defined as a 4-day time span in which photos have been taken, though this can be changed - see *"Adjust event distance"*. If no date from the past can be detected, these JPGs are put into one folder to be sorted manually.

## Origin and Credits

This is a fork of tfrdidi's [much-improved fork](https://github.com/tfrdidi/sort-PhotorecRecoveredFiles) of Chris Masterson's [sort-PhotorecRecoveredFiles](https://github.com/ChrisMagnuson/sort-PhotorecRecoveredFiles). The code of this version is unchanged from tifrdidi's version, and was created purely for the purpose of enabling issue tracking and logging the issues I've come across during usage in the hope that others more adept than me at Python can either add to them or fix them. The bulk of this readme was also written by tfrdidi, and I slightly improved the English for the purpose of making it a little clearer.

## Usage

```python recovery.py <path to files recovered by Photorec> <destination>```

This copies the recovered files to their file type folder in the destination directory. The recovered files are not modified. If a file already exists in the destination directory, it is skipped. This means that the program can be interrupted with Ctrl+C and then continued at a later point by running it again.

The first output of the programm is the number of files to copy. Counting them may take anything from a few minutes to a few hours depending on the amount of recovered files. After that, the program will output feedback every ~2000 processed files.

All directories contain a maximum of 500 files by default. If there are more for a file type, numbered subdirectories are created. If you want another file-limit, e.g. 1000, pass that number as the third parameter when running the program:

```python recovery.py <path to files recovered by Photorec> <destination> 1000```

## Adjust event distance

By default, an event is defined as a 4-day time span in which photos have been taken. If you want to reduce or increase this, simply adjust the variable ```minEventDelta``` in ```jpgHelper.py```. This variable contains the delta between events in seconds. 
