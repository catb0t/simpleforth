#!/usr/bin/env python3

from sys import argv
import os

def main():
    if len(argv) > 1:
        fname = argv[-1]
        try:
            os.stat(fname)
        except (IOError, FileNotFoundError) as err:
            print(err)
            print("stat: cannot stat '{}': no such file or directory")
            exit(2)
        else:
            f = open(fname, 'rt')
            fcont = f.read()
            f.close()
            run(list(fcont))
    else:
        interpret()

def interpret():
    print("\n\tsimpleforth interpreter test repl\n")
    while True:
        print("> ", end="")
        