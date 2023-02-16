#!/usr/bin/env python3

import subprocess
subprocess.run(['touch /tmp/soahzf'],shell=True)
subprocess.run('/challenge/embryoio_level27',stdout=open('/tmp/soahzf', 'w'))