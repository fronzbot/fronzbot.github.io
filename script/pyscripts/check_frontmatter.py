#!/usr/bin/env python
"""
check_frontmatter.py
Author: Kevin Fronczak
Date: July 25, 2017

Usage:
    python3 check_frontmatter.py [tests]

Implemented tests:
    --skip=item1,item2  :  Sets files to be skipped
    - tags  :  Checks for valid tags in each post_vars
    - feature-key  :  Checks that 'feature_image' key is set in a post if it's marked to be featured

"""

import os
import glob
import sys
import re
import helpers
from helpers import (PRINT_OK, PRINT_FAIL, COLOR)
from helpers import print_errors as ERRPRINT


VALID_TAGS = ['analog', 'theory', 'systems', 'circuits', 'projects', 'university project', 'fun',
              'python', 'scripts', 'MATLAB', 'device physics', 'admin', 'home automation', 'noise',
              'signals', 'digital', 'website', 'server', 'unraid', 'linux'
             ]

PRINT_FILE_STRING = None

def main(test_args, skip_list):
    errCount = 0
    file_list = helpers.get_posts()
    for filename in file_list:
        if re.sub(helpers.PATH, '', filename) not in skip_list:
            test_array = list()
            PRINT_FILE_STRING = COLOR.colorize(filename, 'text')
            print(PRINT_FILE_STRING, end=" - ")
            test_err_list = list()
            for arg in test_args:
                (test_errs, test_err_list) = run_test(filename, arg)
                errCount += test_errs
                test_array.append(test_err_list)
            print('')
            for error in test_err_list:
                print(error)

    ERRPRINT(errCount, completion=True)

    return(0)


def run_test(filename, test_name):
    '''Runs given test by first extracting frontmatter from file.'''
    errCount = 0
    frontmatter, errCount, errList = get_frontmatter(filename, errCount)
    if errCount > 0:
        return errCount, errList

    if test_name == 'feature-key':
        (test_err, error_list) = check_feature_key(frontmatter)
        errCount += test_err
    elif test_name == 'tags':
        (test_err, error_list) = check_tags(frontmatter)
        errCount += test_err
    else:
        print(COLOR.colorize('Unknown test "{}"'.format(test_name), 'error'))
        sys.exit(1)

    return (errCount, error_list)

def get_frontmatter(filename, errCount):
    '''Extracts frontmatter from post for further processing.'''
    post_vars = dict()
    start_read = False
    errList = list()
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip() == '---' and start_read:
                    start_read = False
                    break

                if start_read:
                    line_split = line.split(':')
                    if line_split[0] == 'tags':
                        post_vars[line_split[0]] = list()
                    elif len(line_split) < 2 and 'tags' in post_vars.keys():
                        tag_name = line_split[0].split('-')
                        post_vars['tags'].append(tag_name[1].strip())
                    else:
                        post_vars[line_split[0]] = line_split[1].strip()

                if line.strip() == '---' and not start_read:
                    start_read = True
    except Exception as e:
        errCount += 1
        errList.append(COLOR.colorize("ERROR: {}".format(e), 'error'))

    return post_vars, errCount, errList


def check_tags(frontmatter):
    '''Checks tags in frontmatter against VALID_TAGS list.'''
    errCount = 0
    error_list = list()
    try:
        if not frontmatter['tags']:
            error_list.append(COLOR.colorize('WARNING: "tag" list empty in frontmatter', 'warn'))
        for tag in frontmatter['tags']:
            if tag not in VALID_TAGS:
                errCount += 1
                error_list.append(COLOR.colorize('ERROR: {} is not a valid tag'.format(tag), 'error'))
    except KeyError:
        errCount += 1
        error_list.append(COLOR.colorize('ERROR: "tag" key not found in frontmatter', 'error'))
    except Exception as e:
        errCount += 1
        error_list.append(COLOR.colorize('ERROR: {}'.format(e), 'error'))

    ERRPRINT(errCount, test_name='tags')

    return (errCount, error_list)


def check_feature_key(frontmatter):
    '''Verifies feature_image set if the post is set to be featured.'''
    errCount = 0
    error_list = list()

    if 'project' in frontmatter.keys():
        try:
            is_project  = frontmatter['project']
            is_featured = frontmatter['feature']
        except KeyError:
            is_featured = False
            error_list.append(COLOR.colorize('ERROR: "feature" key not found', 'error'))
            errCount += 1

        try:
            if is_featured == 'true':
                feature_image = frontmatter['feature_image']
        except KeyError:
            error_list.append(COLOR.colorize('ERROR: "feature_image" key not found and "feature" is set to {}'.format(is_featured), 'error'))
            errCount += 1
        except IndexError:
            errCount += 1
            error_list.append(COLOR.colorize('ERROR: Marked as a project but the "feature" key is not set', 'error'))
        except Exception as e:
            errCount += 1
            error_list.append(COLOR.colorize('ERROR: {}'.format(e), 'error'))
    else:
        errCount += 1
        error_list.append(COLOR.colorize('ERROR: Missing "project" key', 'error'))

    ERRPRINT(errCount, test_name='feature_key')

    return (errCount, error_list)

if __name__ == '__main__':
    test_args = list()
    skip_list = list()
    if len(sys.argv) < 2:
        print(COLOR.colorize('ERROR: Requires test argument', 'error'))
        sys.exit(1)
    else:
        for arg in sys.argv[1:]:
            if '--skip=' in arg:
                comma_list = arg.split('--skip=')
                skip_list = comma_list[1].split(',')
            else:
                test_args.append(arg)

    main(test_args, skip_list)
