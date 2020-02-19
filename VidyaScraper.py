#!/usr/bin/python3
try:
    import requests
    import argparse
    import shutil
    import json
    import os
    import re
except ImportError as e:
    print('Missing needed Module\nError:\n' + str(e))
    print('\nPlease install any missing modules.\nExiting')
    exit()

# Argparse Stuff.
par = argparse.ArgumentParser(description="Vidya Scraper.")
par.add_argument('post', nargs='*', default=False, type=str, help='Post to download info from.')
pargs = par.parse_args()


# import variable shortners:
r = requests
j = json
s = shutil

# Test Urls:
# url = 'https://vidyart.booru.org/index.php?page=post&s=view&id=377861'
# url1 = 'https://vidyart.booru.org/index.php?page=post&s=view&id=376759'

# Json Output File.
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
def download_file(iurl, din):
    ftype = iurl.split('.')[-1]
    local_filename = str(din) + '.' + str(ftype)
    with requests.get(iurl, stream=True) as r:
        with open(local_filename, 'wb') as f:
            s.copyfileobj(r.raw, f)
    return local_filename


# Building Post URL:
url = str('https://vidyart.booru.org/index.php?page=post&s=view&id=' + thing)

# Grab pages RAW output:
t = r.get(url)

# Test if page is 200 else skip/end.
if str(200) in str(t):
    print(True)
    pass
else:
    print(False)
    exit()

# Parse out wanted information:
# Tags.
tags = re.findall('((?<=post&amp;s=list&amp;tags=)\S*)+"', t.text)
n = (len(tags) - 1)
del(tags[n])
del(tags[0])
# Direct image link.
img = re.findall('((?<=id="note-container"><img alt="img" src=")\S*)+"', t.text)
img = img[0]
# Image ID.
id = re.findall('(?<=Id: )(\S*)', t.text)
id = id[0]
# Date/Time Posted.
posted = re.findall('(?<=Posted: )(\S*)(.+)(\S*)<+', t.text)
date = posted[0][0]
time = posted[0][1].strip()
# Uploader.
by = re.findall('(?<=By: )(\S*)', t.text)
by = by[0]
# Image size.
ims = re.findall('(?<=Size: )(\S*)', t.text)
ims = ims[0]
# Image Rating.
irate = re.findall('(?<=Rating: )(\S*)', t.text)
irate = irate[0]
# Score.
scor = re.findall('(?<=Score: )(\S*)', t.text)
scor = scor[0]

# Build Printable CLI output for user:
ptable = ('ID: ' + str(id),
          'Uploader: ' + str(by),
          'Date: ' + str(date),
          'Time: ' + str(time),
          'Image: ' + str(img),
          'Size: ' + str(ims),
          'Rating: ' + str(irate),
          'Score: ' + str(scor),
          'Tags: ' + str(tags)
          )
# Loop through above output.
for d in ptable:
    print(str(d))

# Download image call and provide Rename ID:
download_file(img, id)

# Build Json to output to file.
yd = {'ID': {id: {'uploader': by, 'date': date, 'time': time, 'image': img, 'size': ims, 'rating': irate,
                  'score': scor, 'tags': tags}}}

# Write out to JSON File.
# If json file exist:
if os.path.exists(ydf) is True:
    with open(ydf, 'r+') as f:
        data = j.load(f)
        data['ID'].update(yd['ID'])
        with open(ydf, 'w') as o:
            j.dump(data, o, indent=2, sort_keys=True)
# If json file does not exist.
else:
    with open(ydf, 'w') as f:
        j.dump(yd, f, indent=2, sort_keys=True)
