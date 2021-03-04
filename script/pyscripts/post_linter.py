#!/usr/bin/env python
"""
post_linter.py
Author: Kevin Fronczak
Date: July 27, 2017

Usage:
    python3 post_linter.py [opts]

Options:
    --ignore [list]       :  Allow tags given in 'list'
    --skip-html           :  Skips checking html
    --center-images       :  Verifies markdown tag to center images exists in file
    --center-eqs          :  Verifies non-inline equations are centered
    --image-tag [string]  :  Check if image tags have been updated
    --skip-eq-tags        :  Skip checking of eq tags

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
    found_tags = dict()
    errCount = 0
    if not extra_args['skip-html']:
        print(COLOR.colorize('Checking for errant HTML tags', 'info'), end=' ')
        errs_here = 0
        for filename in file_list:
            (html_found, errs) = get_html(filename, ignore_list)
            html_strings = helpers.merge_dicts(html_strings, html_found)
            errs_here += errs
            errCount += errs
        if errs_here > 0:
            print(PRINT_FAIL)
        for key, entry in html_strings.items():
            if entry:
                print('{}\n{}'.format(key, PRINT_ERROR))
                for element in entry:
                    print('{}: {}'.format(element[0], element[1]))
                print('')
        if errs_here == 0:
            print(PRINT_OK)

    if extra_args['img-tag']:
        tag = extra_args['img-tag']
        print(COLOR.colorize('\nVerifying all image tags have been updated', 'info'), end= ' ')
        errs_here = 0
        for filename in file_list:
            (found, errs) = check_image_tags(filename, tag)
            found_tags = helpers.merge_dicts(found, found_tags)
            errs_here += errs
            errCount += errs
        if errs_here > 0:
            print(PRINT_FAIL)
        for key, entry in found_tags.items():
            if entry:
                print(f"{key}\n{PRINT_ERROR}")
                for element in entry:
                    print(f"{element[0]}: {element[1]}", end='')
        if errs_here == 0:
            print(PRINT_OK)
        else:
            print(COLOR.colorize('Must run ./script/gen_img!', 'warn'))

    if extra_args['center-image']:
        print(COLOR.colorize('\nVerifying images are centered', 'info'), end=' ')
        errs_here = 0
        for filename in file_list:
            (found, errs) = check_image_centering(filename)
            non_centered = helpers.merge_dicts(found, non_centered)
            errs_here += errs
            errCount += errs
        if errs_here > 0:
            print(PRINT_FAIL)
        for key, entry in non_centered.items():
            if entry:
                print('{}\n{}'.format(key, PRINT_ERROR))
                for element in entry:
                    print('{}: {}'.format(element[0], element[1]), end='')
        if errs_here == 0:
            print(PRINT_OK)

    if extra_args['center-eqs']:
        non_centered = dict()
        errs_here = 0
        print(COLOR.colorize('\nVerifying equations are centered', 'info'), end=' ')
        for filename in file_list:
            (found, errs) = check_eq_centering(filename)
            non_centered = helpers.merge_dicts(found, non_centered)
            errs_here += errs
            errCount += errs
        if errs_here > 0:
            print(PRINT_FAIL)
        for key, entry in non_centered.items():
            if entry:
                print('{}\n{}'.format(key, PRINT_ERROR))
                for element in entry:
                    print('{}: {}'.format(element[0], element[1], end=''))
        if errs_here == 0:
            print(PRINT_OK)

    if not extra_args['skip-eq-tags']:
        bad_tags = dict()
        errs_here = 0
        print(COLOR.colorize('\nVerifying equation tags', 'info'), end=' ')
        for filename in file_list:
            (found, errs) = check_old_eq_delim(filename)
            bad_tags = helpers.merge_dicts(found, bad_tags)
            errs_here += errs
            errCount += errs
        if errs_here > 0:
            print(PRINT_FAIL)
        for key, entry in bad_tags.items():
            if entry:
                print('{}\n{}'.format(key, PRINT_ERROR))
                for element in entry:
                    print('{}, '.format(element[0]), end='')
                print()
        if errs_here == 0:
            print(PRINT_OK)

    print('\n')
    ERRPRINT(errCount, completion=True)

    return(0)

def check_eq_centering(filename):
    errs = 0
    line_num = 0
    entries = list()
    with open(filename, 'r') as file:
        for line in file:
            line_num += 1
            match = re.findall('^\+\+.*?\+\+\.$', line)
            if match and '<!-- lint-disable -->' not in line:
                errs += 1
                lnum = COLOR.colorize(str(line_num), 'linenum')
                entry = COLOR.colorize(line, 'error')
                entries.append([lnum, entry])
    return({filename: entries}, errs)

def check_old_eq_delim(filename):
    errs = 0
    line_num = 0
    entries = list()
    with open(filename, 'r') as file:
        for line in file:
            line_num += 1
            match1 = re.findall('^\$\$.*?\$\$\.$', line)
            match2 = re.findall('\$\$.*?\$\$', line)
            match3 = re.findall('\+\+.*?\$', line)
            match4 = re.findall('\$.*?\+\+', line)
            if match1 or match2 or match3 or match4:
                errs += 1
                lnum = COLOR.colorize(str(line_num), 'linenum')
                entry = COLOR.colorize(line, 'error')
                entries.append([lnum, entry])
    return({filename: entries}, errs)

def check_image_tags(filename, tag):
    errs = 0
    line_num = 0
    entries = list()
    with open(filename, 'r') as file:
        for line in file:
            line_num += 1
            if tag in line:
                errs += 1
                lnum = COLOR.colorize(str(line_num), 'linenum')
                entry = COLOR.colorize(line, 'error')
                entries.append([lnum, entry])
    return ({filename: entries}, errs)

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
    extra_args = {}
    extra_args['center-image'] = False
    extra_args['skip-html'] = False
    extra_args['center-eqs'] = False
    extra_args['img-tag'] = False
    extra_args['skip-eq-tags'] = False
    if len(sys.argv) > 1:
        get_ignore_list = False
        for arg in sys.argv:
            if arg == '--center-images':
                get_ignore_list = False
                extra_args['center-image'] = True
            if arg == '--skip-html':
                get_ignore_list = False
                extra_args['skip-html'] = True
            if arg == '--center-eqs':
                get_ignore_list = False
                extra_args['center-eqs'] = True
            if arg == '--skip-eq-tags':
                get_ignore_list = False
                extra_args['skip-eq-tags'] = True
            if get_ignore_list:
                ignore_list.append(arg)
            if arg == '--ignore':
                get_ignore_list = True
            if arg == '--image-tag':
                arg_index = sys.argv.index('--image-tag')
                extra_args['img-tag'] = sys.argv[arg_index + 1]

    main(ignore_list, extra_args)
