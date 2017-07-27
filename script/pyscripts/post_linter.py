"""
post_linter.py
Author: Kevin Fronczak
Date: July 27, 2017

Usage:
    python3 check_images.py [opts]
    
Options:
    --ignore [list]  :  Allow tags given in 'list'
    --skip-html      :  Skips checking html
    --center-images  :  Verifies markdown tag to center images exists in file
    
Runs through posts to find image tags and throws error if html tags are found

"""

import os
import glob
import sys
import re
import helpers
from helpers import (PRINT_OK, PRINT_FAIL, PRINT_ERROR, COLOR)
from helpers import print_errors as ERRPRINT

PRINT_FILE_STRING = None

def main(ignore_list, extra_args):
    file_list = helpers.get_posts()
    html_strings = dict()
    non_centered = dict()
    errCount = 0
    if 'skip-html' not in extra_args:
        print(COLOR.colorize('Checking for errant HTML tags', 'info'), end='\n\n')
        for filename in file_list:
            (html_found, errs) = get_html(filename, ignore_list)
            html_strings = helpers.merge_dicts(html_strings, html_found)
            errCount += errs
        for key, entry in html_strings.items():
            if entry:
                print('{}\n{}'.format(key, PRINT_ERROR))
                for element in entry:
                    print('{}: {}'.format(element[0], element[1]))
                print('')
    
    if 'center-image' in extra_args:
        print(COLOR.colorize('\nVerifying images are centered', 'info'), end='\n\n')
        for filename in file_list:
            (found, errs) = check_image_centering(filename)
            non_centered = helpers.merge_dicts(found, non_centered)
            errCount += errs
        for key, entry in non_centered.items():
            if entry:
                print('{}\n{}'.format(key, PRINT_ERROR))
                for element in entry:
                    print('{}: {}'.format(element[0], element[1]), end='')
    print('\n')
    ERRPRINT(errCount, completion=True)
    
    return(0)
    
def check_image_centering(filename):
    errs = 0
    line_num = 0
    entries = list()
    with open(filename, 'r') as file:
        last_line = ''
        for line in file:
            line_num += 1
            if 'site.image_path' in line:
                if last_line.strip() != '{: .center}':
                    errs += 1
                    lnum = COLOR.colorize(str(line_num), 'linenum')
                    entry = COLOR.colorize(line, 'error')
                    entries.append([lnum, entry])
            last_line = line
            
    return ({filename: entries}, errs)

def get_html(filename, ignore_list):
    '''Extracts html tags from file.'''
    html_strings = list()
    html_found = dict()
    line_number = 0
    errs = 0
    with open(filename, 'r') as file:
        for line in file:
            line_number += 1
            matches = re.findall('<.*?>', line)
            for m in matches:
                if any(tag in m for tag in ignore_list):
                    pass
                elif '<!-- lint-disable -->' in line:
                    pass
                else:
                    errs += 1
                    lnum = COLOR.colorize(str(line_number), 'linenum')
                    match = COLOR.colorize(m, 'error')
                    html_strings.append([lnum, match])

    html_found[filename] = html_strings
    return (html_found, errs)

if __name__ == "__main__":
    ignore_list = []
    extra_args = []
    if len(sys.argv) > 1:
        get_ignore_list = False
        for arg in sys.argv:
            if arg == '--center-images':
                get_ignore_list = False
                extra_args.append('center-image')
            if arg == '--skip-html':
                get_ignore_list = False
                extra_args.append('skip-html')
            if get_ignore_list:
                ignore_list.append(arg)
            if arg == '--ignore':
                get_ignore_list = True

    main(ignore_list, extra_args)
