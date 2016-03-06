#!/usr/bin/env python3

from sys    import argv
from pmlr   import pmlr
from time   import sleep
from forth  import Forth
from docopt import docopt

print       = pmlr.util.writer
debug_write = pmlr.util.debug_write


def main():
    pmlr.DEBUG = True
    pmlr.init()
    if len(argv) > 1:
        fromfile(argv[-1])
    else:
        interpret(argv)


def fromfile(name, args):
    fth = Forth()
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
        fth.run(list(fcont))


def interpret(args):
    print("\n\tsimpleforth interpreter: test repl\n")
    fth = Forth()

    while True:
        print("> ")
        f = pmlr.readkey()
        print(f)

        if f == ":":
            print("\x1b[1A\x1b[50C\x1b[1;31mCOMPILE\x1b[56D\x1b[1B\x1b[0m")
            colexpr = pmlr.until(";")
            print(";\n")

            # removes "" empty string
            defn = [
                i for i in " ".join(colexpr.split(" ")).split(" ")
                if i != ""
            ]
            # words need names
            if not defn: print("can't compile empty NOP word without a name\n"); continue
            # empty words are ok, as long as they're named
            elif len(defn) == 1: name, rst = defn[0], "NOP"
            # normal, defined words
            else: name, rst = " ".join(defn[1:]), defn[0]

            print(
                " {0} -> \n\t{1}\n compile new word {0} ? (y/N) "
                .format(name, rst)
            )

            if pmlr.readkey().lower() in ("y", "\n", " "):

                err = fth.define(name, rst)
                for i in "compiling...":
                    sleep(.06)
                    print(i)

                if err:
                    print(
                        " compilation finished with errors :(\n error {}: {}"
                        .format(err["name"], err["desc"])
                    )
                else:
                    print("done!")
            else:
                print("\n word not compiled.")

        else:
            print("\x1b[1A\x1b[50C\x1b[1;34mINTERPRET\x1b[59D\x1b[1B\x1b[0m")
            prog = f + pmlr.until("\n")
            #print("\n" + prog)
            fth.run(prog)

        print("\n")


if __name__ == '__main__':
    main()
