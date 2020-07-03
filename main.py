#!/usr/bin/python3

from config import *
import time
import os

print('Option Select File for Vidya Booru Scraper.')
print('')
print('Please select one of the following options:')
print('1. Download a specific image #.')
print('2. Download a range of image #s.')
print('3. Download starting from a specific image #.')
print('4. Download starting from last known downloaded image.')
thing = input()

# Grab the directories working path:
wd = os.path.dirname(__file__)

# last download file location:
last = wd + '/last.txt'


def vidyascraper(id):
    os.system("py " + wd + "/VidyaScraper.py " + str(id))


# Adding rate-limit to prevent over requesting
def ratelimit(rl):
    if RateLimit > 0:
        print('Rate-Limit: ' + str(rl) + ' seconds.')
        time.sleep(rl)


def lastdownload(file, lid):
    lfile = open(file, 'w')
    if os.path.isfile(last) is False:
        lfile.write(lid)
    else:
        lfile.write(lid)
    lfile.close()


if int(thing) == 1:
    print('Please provide a Image # that you want to download.')
    postID = input()
    vidyascraper(postID)
    lastdownload(last, str(postID))
elif int(thing) == 2:
    print('Please provide the Image number you want to start with.')
    firstPostId = int(input())
    print('Please provide the Image number you want to end with.')
    lastPostId = int(input()) + 1
    for i in range(firstPostId, lastPostId):
        vidyascraper(i)
        lastdownload(last, str(i))
        ratelimit(RateLimit)
elif int(thing) == 3:
    print('Please provide the image number to start at.')
    startPostId = input()
    try:
        postID = startPostId
        while True:
            print('Attempting PostID: ' + str(postID))
            vidyascraper(str(postID))
            lastdownload(last, str(postID))
            ratelimit(RateLimit)
            postID = int(postID) + 1
    except KeyboardInterrupt:
        print('User Interrupted')
        exit()
elif int(thing) == 4:
    print('Loading last known download from "last.txt"')
    lopen = open(last, 'r')
    lastPostID = lopen.read()
    print('Last Image # Downloaded: ' + str(lastPostID))
    print('Do you wish to continue? (y/n)')
    yesno = input()
    if yesno == 'y':
        pass
    else:
        print('exiting')
        exit()
    nextPostID = int(lastPostID) + 1
    try:
        while True:
            print('Attempting PostID: ' + str(nextPostID))
            vidyascraper(str(nextPostID))
            lastdownload(last, str(nextPostID))
            ratelimit(RateLimit)
            nextPostID = int(nextPostID + 1)
    except KeyboardInterrupt:
        print('User Interrupted')
else:
    print('Please provide a valid option.')
