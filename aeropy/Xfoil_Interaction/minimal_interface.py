import subprocess
import sys

commands = ['naca 6715',
            'oper',
            'mach 0.2',
            're 3500',
            'alfa 3']

p = subprocess.Popen(["xfoil.exe",],
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)

for command in commands:
     p.stdin.write((command + '\n').encode())

p.stdin.write("\nquit\n".encode())
p.stdin.close()
for line in p.stdout.readlines():
    print(line.decode(), end='')
