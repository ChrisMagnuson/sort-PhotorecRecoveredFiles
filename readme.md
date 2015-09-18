# Sort files recoverd by Photorec

Photorec does a great job when recovering deleted files. But the result is a huge unsorted unnamed amount of files. Especially for external hard drives which serve as backup of all personal data, sortig them is an endless job.

This program helps you sorting your files. First of all, the files are copied to own folders for each file type. Second, jpegs are distinguished by the year when they have been taken and by the event. We thereby define an event as a time span during them photos are shot and that has at least a time span of 4 days without a photo to another event. 


## Usage

```python recovery.py <path to files recovered by Photorec> <destination>```

This copies the recovered file to their file type folder in the destination directory. The recovered files are not modified.


## Adjust event distance

For the case you want to reduce or increase the timespan between events, simply adjust the variable ```minEventDelta```. This variable contains the delta between events in seconds. 