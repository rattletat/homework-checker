#!/bin/bash/python3
import sys
import subprocess

separator = sys.argv[1]

output = subprocess.run(
    ["pytest", "--tap-stream", "tests.py"], capture_output=True, text=True
).stdout

print(separator)
print(output)
print(separator)
