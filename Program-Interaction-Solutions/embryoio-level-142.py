import os
import sys

sock_fd = sys.argv[1]
pr = os.fdopen(int(sock_fd), 'r')

while line := pr.readline():
    print(line)

    chal = line.find('for: ')
    if chal > 0:
        os.write(int(sock_fd), str(eval(line[chal+4:].strip())).encode() + b'\n')