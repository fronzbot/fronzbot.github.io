#!/usr/bin/env python
"""
tag_gen.py
Author: Kevin Fronczak
Date: Dec 23, 2017
"""

import sys
import os
import glob
from helpers import VALID_TAGS, COLOR
from helpers import print_errors as ERRPRINT

BASEDIR = '/home/kevin/Projects/fronzbot.github.io'
POSTDIR = '_posts/'
TAGDIR = 'tag/'

post_dir = os.path.join(BASEDIR, POSTDIR)
tag_dir = os.path.join(BASEDIR, TAGDIR)

def main(debug, checker=False):
    """Method to get list of tags."""
    all_posts = glob.glob("{}*.md".format(post_dir))
    all_tags = list()

    old_tags = glob.glob("{}*.md".format(tag_dir))
    
    if checker:
        errorCount = 0
        existing_tag_pages = list()
        for tag in old_tags:
            tagfile = os.path.basename(tag)
            tagname, ext = os.path.splitext(tagfile)
            existing_tag_pages.append(tagname)
        for valid_tag in VALID_TAGS:
            if valid_tag not in existing_tag_pages:
                print(COLOR.colorize("Missing tag page {}".format(valid_tag), 'error'))
                errorCount += 1
        ERRPRINT(errorCount, completion=True)
        sys.exit(0) 
    else:
        for tag in old_tags:
            os.remove(tag)

        for tag in VALID_TAGS:
            tag_file = '{}{}.md'.format(tag_dir, tag)
            if debug:
                print("Generating {} tag page".format(tag_file))
            with open(tag_file, 'w') as ftag:
                out_str = "---\nlayout: tagpage\ntitle: \"Tag: {}\"\ntag: {}\nrobots: noindex\n---\n".format(tag, tag)
                ftag.write(out_str)
    
        print('Generated {} Tags'.format(VALID_TAGS.__len__()))


if __name__ == '__main__':
    debug = False
    checker = False
    if '--debug' in sys.argv:
        debug=True
    if '--check' in sys.argv:
        main(debug, checker=True)
    main(debug)
