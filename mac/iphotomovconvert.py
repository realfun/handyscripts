#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
from datetime import datetime


def print_usage():
    print("""
       Usage:
           iphotomovconvert.py -t
              dry run

           iphotomovconvert.py -o <output-folder>
              real convert, after convert all the stuff will be stored in output folder.
              user need to import these photos back to iPhoto
    """)


# -----------------------------
#  command line parsing
# -----------------------------
if len(sys.argv) <= 1:
    print_usage()
    sys.exit(0)

OUTPUT_DIR_CONTAINER = '/tmp/iphotoconvert/'
if sys.argv[1] == '-t':
    pass
elif sys.argv[1] == '-o' and len(sys.argv) == 3:
    OUTPUT_DIR_CONTAINER = sys.argv[2]
else:
    print_usage()
    sys.exit(0)


def get_rotation(mov_file):
    output = subprocess.check_output(['exiftool', '-j', mov_file])
    # noqa pylint: disable=invalid-name
    js = json.loads(output)
    rot = js[0].get('Rotation') or js[0].get('rotation')
    if rot:
        # print js, rot
        # http://superuser.com/questions/418985/can-handbrake-flip-rotate-a-video
        if rot == 180:
            return 0
        if rot == 90:
            return 1
        if rot == 270:
            return 2
        print(f'unknown rotation {rot} for file {mov_file}')
    return 0


# -----------------------------
#  get the list of MOV files
# -----------------------------
src_dir = os.path.join(os.environ['HOME'], 'Pictures/iPhoto Library/Masters')
dest_dir = os.path.join(OUTPUT_DIR_CONTAINER, datetime.now().strftime("%Y%m%d_%H%M%S"))

# print 'Converting photos from [', src_dir, '] to [', dest_dir, ']'

job_list = []
dirs_to_create = set()
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.lower().endswith('.mov'):
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_dir, src_file_path[len(src_dir)+1:-4] + '.mp4')
            job_list.append((src_file_path, dest_file_path))
            dirs_to_create.add(os.path.dirname(dest_file_path))

for d in dirs_to_create:
    print('mkdir -p "' + d + '"')

i = 0
for s, d in job_list:
    i += 1
    # noqa pylint: disable=invalid-name
    r = get_rotation(s)
    rotate = '' if not r else (f'-vf "transpose={r}"')
    # ffmpeg -i "IMG_0618.MOV" -vcodec copy -acodec copy -vf "transpose=1" "20140615-224542.mp4"
    cmd = 'ffmpeg -i "' + s + '" ' + rotate + ' "' + d + '"'
    print('echo', cmd)
    print(f'echo "--------------- processing [{i}/{len(job_list)}] ---------------"')
    print(cmd)
    print('touch -r "' + s + '" "' + d + '"')
    print(f'echo "--------------- processing [{i}/{len(job_list)}] ---------------"')
