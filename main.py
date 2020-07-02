#!/usr/bin/python3

from config import *
import time
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


def vidyascraper(ID):
    os.system("py " + wd + "/VidyaScraper.py " + str(ID))


# Adding rate-limit to prevent over requesting
def ratelimit(rl):
    if RateLimit > 0:
        print('Sleeping for ' + str(rl) + ' seconds for Rate-Limit.')
        time.sleep(rl)


if int(thing) == 1:
    print('Please provide a Image # that you want to download.')
    postID = input()
    vidyascraper(postID)
elif int(thing) == 2:
    print('Please provide the Image number you want to start at.')
    firstPostId = int(input())
    print('Please provide the Image number you want to end at.')
    lastPostId = int(input()) + 1
    for i in range(firstPostId, lastPostId):
        vidyascraper(i)
        ratelimit(RateLimit)
