'''Various helper functions and classes'''
import glob
import sys

PATH = './_posts/'
EXT = '.md'

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
