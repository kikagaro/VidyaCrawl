#!/usr/bin/python3

import os

print('Option Select File for Vidya Booru Scraper.')

print('Please select one of the following options:')
print('1. Download a specific image #.')
print('2. Download a range of image #s.')
print('3. Download from a specific image # to current #.')
print('4. Download images starting from Post ID 1.')
print('5. Download from the last known image saved.')
thing = input()

# Grab the directories working path:
wd = os.path.dirname(__file__)

if int(thing) == 1:
    print('Please provide a Image # that you want to download.')
    postID = input()
#    exec(open("VidyaScraper.py").read())
    os.system("py " + wd + "/VidyaScraper.py " + postID)
