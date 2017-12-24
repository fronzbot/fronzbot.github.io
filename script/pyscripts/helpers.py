'''Various helper functions and classes'''
import glob
import sys

PATH = './_posts/'
EXT = '.md'

VALID_TAGS = ['analog', 'theory', 'systems', 'circuits', 'projects', 'university project', 'fun',
              'python', 'scripts', 'MATLAB', 'device physics', 'admin', 'home automation', 'noise',
              'signals', 'digital', 'website', 'server'
             ]

class ColorLog(object):
    '''Class to colorize log output'''

    def __init__(self):
        from colorama import init, Fore
       
        init(autoreset=True)
        self.colors = {'error': Fore.RED,
                       'warn': Fore.YELLOW,
                       'ok': Fore.GREEN,
                       'text': Fore.WHITE,
                       'fail': Fore.RED,
                       'pass': Fore.GREEN,
                       'info': Fore.WHITE,
                       'linenum': Fore.CYAN
                      }

    def colorize(self, string, type):
        try:
            return (self.colors[type] + string)
        except KeyError:
            print('Unkown key {}'.format(type))
            sys.exit(1)

COLOR = ColorLog()
PRINT_OK = COLOR.colorize('OK', 'ok')
PRINT_FAIL = COLOR.colorize('FAIL', 'fail')
PRINT_ERROR = COLOR.colorize('ERROR:', 'error')

def print_errors(errCount, test_name=None, completion=False):
    if completion:
        if errCount > 0:
            print(COLOR.colorize('FAILED :( with {} total errors'.format(errCount), 'fail'), end='\n\n')
            sys.exit(1)
        else:
            print(COLOR.colorize('PASSED :)', 'pass'), end='\n\n')
    else:
        if errCount > 0:
            print('{}: {}'.format(test_name,  PRINT_FAIL), end='  ')
        else:
            print('{}: {}'.format(test_name, PRINT_OK), end='  ')


def get_posts():
    return glob.glob('{}*{}'.format(PATH, EXT))

def merge_dicts(first, second):
    """Merges two dictionaries and errors if keys are the same."""
    for key in first:
        if key in second:
            raise KeyError('Matching keys in dicts trying to be merged.')

    merged = first.copy()
    merged.update(second)
    return merged

def get_frontmatter(filename, error_check=True):
    """Returns frontmatter of file."""
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

    if error_check:
        return post_vars, errCount, errList

    return post_vars
