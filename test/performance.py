import os
import shutil
import imp
from functools import wraps
from timeit import repeat

size = [1, 10, 100, 1000, 10000]
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
def performance(name, size, number=1):

    # Subtitute of shutil.copytree which gives an error
    def copytree(src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d)
            else:
                if not os.path.exists(d) or \
                        os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                    shutil.copy2(s, d)

    test_path = os.path.join(os.getcwd(), test_folder)
    os.chdir(name)
    copied = os.listdir()
    copytree(os.getcwd(), test_path)
    os.chdir(test_path)

    try:
        atm
    except NameError:
        import isa
    imp.reload(isa)

    times = []
    for element in size:
        element = int(element)
        if element == 1:
            time = repeat('atm(0.)', setup='from isa import atm',
                          number=number, repeat=3)
        elif element > 1:
            time = repeat('atm(h)',
                          setup='from isa import atm\n'
                                'from numpy import linspace\n'
                                'h = linspace(0., 11000., {})'
                                .format(element),
                          number=number, repeat=3)
        time = 1e3 * min(time) / number
        times.append(time)

    for item in copied:
        if(os.path.isdir(item)):
            shutil.rmtree(item)
        else:
            os.remove(item)

    return times


if __name__ == '__main__':

    test = dict()
    for name in get_folders():
        print('{} running...'.format(name))
        test[name] = performance(name, size)

    line = 'size    '
    name = None
    for name in test.keys():
        line += '{:<15} '.format(name)
    if name is not None:
        print(line)
        for i in range(0, len(test[name])):
            line = '{:>7} '.format(size[i])
            for name in test.keys():
                line += '{:12.3f} ms '.format(test[name][i])
            print(line)
    else:
        print('No files found.')
