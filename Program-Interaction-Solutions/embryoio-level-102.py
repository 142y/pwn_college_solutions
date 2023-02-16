import glob
import time

bin_path = glob.glob('/challenge/em*')[0]

p = process(argv='cziyrd', executable=bin_path)

time.sleep(1)
print(p.read(4096).decode())