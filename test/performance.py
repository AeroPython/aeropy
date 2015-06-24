import os
import sys
from importlib import reload
from functools import wraps
from timeit import repeat
from collections import OrderedDict

size = [1, 10, 100, 1000, 10000, 100000]
ignore_folders = ['.git', 'test']
test_folder = 'test'


def path_to_project(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        current = os.getcwd()
        filename = os.path.basename(__file__)
        test_path = os.path.abspath(__file__)[: -(1 + len(filename))]

        os.chdir(test_path)
        os.chdir('..')
        value = function(*args, **kwargs)
        os.chdir(current)

        return value
    return wrapper


@path_to_project
def get_folders():
    folders = []
    for folder in os.listdir():
        if(os.path.isdir(folder) and (folder not in ignore_folders)):
            folders.append(folder)
    return folders


@path_to_project
def performance(name, size, loops=100):

    libpath = os.path.join(os.getcwd(), name)
    sys.path.append(libpath)

    try:
        atm
    except NameError:
        import isa
    reload(isa)

    times = []
    for element in size:
        element = int(element)
        if element == 1:
            time = repeat('atm(0.)', setup='from isa import atm',
                          number=loops, repeat=3)
        elif element > 1:
            time = repeat('atm(h)',
                          setup='from isa import atm\n'
                                'from numpy import linspace\n'
                                'h = linspace(0., 11000., {})'
                                .format(element),
                          number=loops, repeat=3)
        time = 1e3 * min(time) / loops
        times.append(time)

    sys.path.remove(libpath)

    return times


if __name__ == '__main__':

    print('Testing different ISA atmosphere implementations...')

    test = OrderedDict()
    for name in get_folders():
        print('{} running...'.format(name))
        test[name] = performance(name, size)

    line = '{:>10}'.format('array size')
    name = None
    for name in test.keys():
        line += ' {:>13}'.format(name)
    if name is not None:
        print(line)
        for i in range(0, len(test[name])):
            line = '{:>10}'.format(size[i])
            for name in test.keys():
                line += ' {:10.3f} ms'.format(test[name][i])
            print(line)
    else:
        print('No files found.')
