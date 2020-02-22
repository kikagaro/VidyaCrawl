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
def download_file(iurl, din, ipath):
    ftype = iurl.split('.')[-1]
    local_filename = str(din) + '.' + str(ftype)
    image_path = ipath + '/' + local_filename
    if os.path.isfile(image_path) is False:
        with requests.get(iurl, stream=True) as r:
            with open(image_path, 'wb') as f:
                s.copyfileobj(r.raw, f)
        return local_filename
    else:
        print("The image exist:\n%s\n" % image_path)
        pass


# Folder Check Function:
def folder_check(cfolder):
    if os.path.isdir(cfolder) is False:
        try:
            os.mkdir(cfolder)
        except OSError:
            print("Creation of the directory %s filed." % cfolder)
        else:
            print("Successfully created the directory %s." % cfolder)
    else:
        pass


# Record Deleted Post function:
def deleted_post(poid, burl):
    pjson = {'ID': {poid: {'url': burl}}}
    djson = os.getcwd() + '/deleted.json'
    if os.path.isfile(djson) is False:
        with open(djson, 'w') as f:
            j.dump(pjson, f, indent=2, sort_keys=True)
    else:
        with open(djson, 'r+') as f:
            data = j.load(f)
            data['ID'].update(pjson['ID'])
            with open(djson, 'w') as o:
                j.dump(data, o, indent=2, sort_keys=True)


# Child post check function:
def child_check(rawt):
    childc = re.findall('((?<=This post has <a href=")\S*)+"', rawt)
    if len(childc) >= 1:
        chi = True
    else:
        chi = False
    return chi


# Building Post URL:
url = str('https://vidyart.booru.org/index.php?page=post&s=view&id=' + thing)

# Grab pages RAW output:
t = r.get(url)

# Grab page title:
title = re.findall('<title>/v/idyart</title>', t.text)

# Test if page redirects to posts page.
if len(title) >= 1:
    print('Post link is bad.\nRecording Post ID\n')
    deleted_post(thing, url)
    exit()
else:
    print('Post link is good.\n')
    pass

# Child post check:
child = child_check(t.text)

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
# Source:
sour = re.findall('(?<=Source: )(\S*)', t.text)

# Dynamic Variables
# Related Post IDs from Child Post
if child is True:
    puri = re.findall('((?<=This post has <a href=")\S*)+"', t.text)
    purl = str('https://vidyart.booru.org/' + puri[0])
    ptxt = r.get(purl)
    rid = re.findall('(?<=posts\[)[0-9]*', ptxt.text)
    rid.remove(id)
    print(rid)

# Path Variables for assets
wd = os.getcwd() + '/assets'
yd = date.split('-')[0]
md = date.split('-')[1]
yp = wd + '/' + yd
mp = yp + '/' + md
ydf = mp + '/data.json'


# Check / Creating download path for images:
try:
    folder_check(wd)
    folder_check(yp)
    folder_check(mp)
except:
    print('Folder Check errors.')
    exit()

# Download image call and provide Rename ID:
download_file(img, id, mp)

# Build Json to output to file.
yd = {'ID': {id: {'uploader': by, 'date': date, 'time': time, 'image': img, 'size': ims, 'rating': irate,
                  'score': scor, 'source': sour, 'tags': tags, 'child post': 'no'}}}
# Additional Json if Child is true.
if child is True:
    cyd = {'ID': {id: {'related post': rid, 'child post': 'yes'}}}
    yd['ID'][id].update(cyd['ID'][id])

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
