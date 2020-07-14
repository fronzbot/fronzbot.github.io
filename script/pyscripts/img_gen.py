#!/usr/bin/env python
"""
img_gen.py
Author: Kevin Fronczak
Date: July 14, 2020

Usage:
    python3 img_gen.py [opts]

    Options:
        --tag <string> : image tag to use
        --skip-diff    : Skips manual diff between files

Finds image tag and turns line into a valid image path (ie. [img]/path/file.jpg where [img] is the tag to find)

"""

import os
import glob
import sys
import re
import helpers
from helpers import (PRINT_OK, PRINT_FAIL, PRINT_ERROR, COLOR)
from helpers import print_errors as ERRPRINT

PRINT_FILE_STRING = None
BASE_IMAGE_PATH = "{{ site.url }}{{ site.image_path }}"

def main(extra_args):
    file_list = helpers.get_posts()
    errCount = 0
    tag = extra_args["tag"]
    skip_diff = extra_args["skip_diff"]
    print(COLOR.colorize(f"\nLooking for {tag}\n", "warn"))
    for filename in file_list:
        entries = find_tags(filename, tag)
        if not entries:
            msg = COLOR.colorize("No image tags found", "error")
            print(f"{filename}: {msg}")
            continue
        msg = COLOR.colorize(f"{len(entries)} tags found!", "warn")
        msg2 = COLOR.colorize(f" lines: {list(entries.keys())}", "linenum")
        print(f"{filename}: {msg} {msg2}")
        replace_tags(filename, entries)
        errCount += diff_before_continue(filename, skip_diff)

    print('\n')
    ERRPRINT(errCount, completion=True)
    return(errCount)

def find_tags(filename, tag):
    line_num = 0
    entries = dict()
    with open(filename, 'r') as _file:
        for line in _file:
            line_num += 1
            if tag in line:
                split_line = line.split(tag)
                image_path = split_line[1].strip()
                start = "[![{{ site.url }}]"
                image_url = f"{BASE_IMAGE_PATH}{image_path}"
                full_image_link = f"{start}({image_url})]({image_url})"
                center_tag = "{: .center}"
                new_line = f"{center_tag}\n{full_image_link}\n"

                entries[line_num] = new_line

    return entries

def replace_tags(filename, entries):
    line_num = 0
    lines_to_write = list()
    with open(filename, 'r') as _file:
        for line in _file:
            line_num += 1
            if line_num in entries:
                lines_to_write.append(entries[line_num])
            else:
                lines_to_write.append(line)
    with open(f"{filename}.bak", 'w') as _file:
        for line in lines_to_write:
            _file.write(line)

def diff_before_continue(filename, skip_diff):
    if not skip_diff:
        print("")
        os.system(f"diff --color {filename} {filename}.bak")
        print("")
        result = input(COLOR.colorize("OK to finalize changes? [y/N]", "warn"))
        print("")
        result_clean = result.lower()
    else:
        result_clean = "y"
    if result_clean == "y":
        os.system(f"mv {filename}.bak {filename}")
        return(0)
    else:
        os.system(f"rm {filename}.bak")
        return(1)

if __name__ == "__main__":
    extra_args = {}
    try:
        tag_index = sys.argv.index("--tag")
        tag = sys.argv[tag_index + 1]
    except IndexError:
        print(COLOR.colorize("Syntax error with custom tag.", "error"))
        sys.exit(1)
    except ValueError:
        tag = "[img]"
    extra_args["tag"] = tag
    extra_args["skip_diff"] = False

    if "--skip-diff" in sys.argv:
        extra_args["skip_diff"] = True

    sys.exit(main(extra_args))
