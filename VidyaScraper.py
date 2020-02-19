#!/usr/bin/python3

import requests
import argparse
import shutil
import json
import os
import re

# Argparse Stuff
par = argparse.ArgumentParse(description="Vidya Scraper.")
par.add_argument('post', nargs='*', default=False, type=str, help='Post to download info from.')
pargs = par.parse_args()


# import variable shortners:
r = requests
j = json
s = shutil

# Test Urls:
# url = 'https://vidyart.booru.org/index.php?page=post&s=view&id=377861'
# url1 = 'https://vidyart.booru.org/index.php?page=post&s=view&id=376759'

# Json Output File
ydf = './data.json'

# Check for post variable:
thing = ''
try:
    thing = pargs.post[0]
except TypeError or NameError:
    print('Post Argument not provided.\n')
    thing = ''
if not thing:
    print('Please provide a post ID')
    thing = input()

# Image Download Function:
def download_file(url, din):
    local_filename = url.split('/')[-1]
    ftype = re.findall('(?<=\.)\S*', local_filename)
    local_filename = str(din) + '.' + str(ftype[0])
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            s.copyfileobj(r.raw, f)
    return local_filename


# Building Post URL:
url = str('https://vidyart.booru.org/index.php?page=post&s=view&id=' + thing)

# Grab pages RAW output:
t = r.get(url)

# Test if page is 200 else skip
if str(200) in str(t):
    print(True)
    pass
else:
    print(False)
    exit()

# Parse out wanted information:
tags = re.findall('((?<=post&amp;s=list&amp;tags=)\S*)+"', t.text)
n = (len(tags) - 1)
del(tags[n])
del(tags[0])
img = re.findall('((?<=id="note-container"><img alt="img" src=")\S*)+"', t.text)
img = img[0]
id = re.findall('(?<=Id: )(\S*)', t.text)
id = id[0]
posted = re.findall('(?<=Posted: )(\S*)(.+)(\S*)<+', t.text)
date = posted[0][0]
time = posted[0][1].strip()

# Build Printable output for user:
ptable = ('ID: ' + str(id),
          'Date: ' + str(date),
          'Time: ' + str(time),
          'Image: ' + str(img),
          'Tags: ' + str(tags)
          )
for d in ptable:
    print(str(d))

# Download image call and provide Rename ID:
download_file(img, id)

# Build Json to output to file.
yd = {'ID': {id: {'date': date, 'time': time, 'image': img, 'tags': tags}}}

# Write out to JSON File.
if os.path.exists(ydf) is True:
    with open(ydf, 'r+') as f:
        data = j.load(f)
        data['ID'].update(yd['ID'])
        with open(ydf, 'w') as o:
            j.dump(data, o, indent=2, sort_keys=True)
else:
    with open(ydf, 'w') as f:
        j.dump(yd, f, indent=2, sort_keys=True)
