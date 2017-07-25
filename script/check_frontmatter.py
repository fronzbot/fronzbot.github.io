import os
import glob
import sys
from colorama import init, Fore

init(autoreset=True)

PATH = './_posts/'
EXT = '.md'

VALID_TAGS = ['analog', 'theory', 'linear systems', 'circuits', 'projects', 'university project', 'fun',
              'python', 'scripts', 'MATLAB'
             ]

PRINT_FILE_STRING = None
PRINT_OK = Fore.GREEN + 'OK'
PRINT_FAIL = Fore.RED + 'FAIL'   
       
def main():
    errCount = 0
    for filename in glob.glob('{}*{}'.format(PATH, EXT)):
        test_array = list()
        print('')
        PRINT_FILE_STRING = Fore.WHITE + filename
        print(PRINT_FILE_STRING, end=" - ")
        for arg in sys.argv[1:]:
            (test_errs, test_err_list) = run_test(filename, arg)
            errCount += test_errs
            test_array.append(test_err_list)
        print('')
        for error in test_err_list:
            print(error)
            

    if errCount > 0:
        print(Fore.RED + 'FAILED :( with {} total errors'.format(errCount))
        sys.exit(1)
    else:
        print(Fore.GREEN + 'PASSED :)')

    return(0)

    
def run_test(filename, test_name):
    errCount = 0
    frontmatter = get_frontmatter(filename)
    if test_name == 'feature_key':
        (test_err, error_list) = check_feature_key(frontmatter)
        errCount += test_err
    elif test_name == 'tags':
        (test_err, error_list) = check_tags(frontmatter)
        errCount += test_err
    else:
        print(Fore.RED + 'Unknown test "{}"'.format(test_name))
        sys.exit(1)

    return (errCount, error_list)

def get_frontmatter(filename):
    post_vars = dict()
    start_read = False
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

    return post_vars


def check_tags(frontmatter):
    errCount = 0
    error_list = list()
    try:
        if not frontmatter['tags']:
            error_list.append(Fore.YELLOW + 'WARNING: "tag" list empty in frontmatter')
        for tag in frontmatter['tags']:
            if tag not in VALID_TAGS:
                errCount += 1
                error_list.append(Fore.RED + 'ERROR: {} is not a valid tag'.format(tag))
    except KeyError:
        errCount += 1
        error_list.append(Fore.RED + 'ERROR: "tag" key not found in frontmatter')

    print_errors('tags', errCount)
    
    return (errCount, error_list)

    
def check_feature_key(frontmatter):
    errCount = 0
    error_list = list()

    if 'project' in frontmatter.keys():
        try:
            is_project  = frontmatter['project']
            is_featured = frontmatter['feature']
        except KeyError:
            is_featured = False
            error_list.append(Fore.RED + 'ERROR: "feature" key not found')
            errCount += 1
            
        try:
            if is_featured == 'true':
                feature_image = frontmatter['feature_image']
        except KeyError:
            error_list.append(Fore.RED + 'ERROR: "feature_image" key not found and "feature" is set to {}'.format(is_featured))
            errCount += 1
        except IndexError:
            error_list.append(Fore.RED + 'ERROR: Marked as a project but the "feature" key is not set')
    else:
        errCount += 1
        error_list.append('ERROR: Missing "project" key')

    print_errors('feature_key', errCount)

    return (errCount, error_list)

def print_errors(test_name, errCount):
    if errCount > 0:
        print('{}: {}'.format(test_name, PRINT_FAIL), end='  ')
    else:
        print('{}: {}'.format(test_name, PRINT_OK), end='  ')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(Fore.RED + 'ERROR: Requires test argument')
        sys.exit(1)
    main()
    