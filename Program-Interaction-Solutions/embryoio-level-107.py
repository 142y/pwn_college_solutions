import glob
import os
import subprocess
import time

bin_path = glob.glob('/challenge/em*')[0]

fd = os.pipe()

os.dup2(fd[0], 55)
p = subprocess.Popen([bin_path], pass_fds=(55,))

os.write(fd[1], b'vrhffjxj')

time.sleep(1)