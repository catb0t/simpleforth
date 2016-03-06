#!/usr/bin/env python3

from pmlr import pmlr

debug_write = pmlr.util.debug_write


def is_none(*args):
    return True if None in args else False


class MalformedExpressionException(Warning):
    pass

    def __init__(*msg, level="INFO"):



class Forth(object):

    def __init__(self):
        self._stack  = Stack()
        self._lopstk = Stack()
        self._retstk = Stack()
        self._sftstk = Stack()

        self.dict = {
            "dup": (self._stack.dup, ())
        }

    def run(self, prog, sandbox=False):
        pass

    def define(self, name, defn):
        defn = " ".join(defn).strip()
        try:
            self.run(defn, sandbox=True)
        except MalformedExpressionException as err:
            debug_write(err, "\n", level=err.level)

        return None  # {"name": "None", "desc": "debug"}


class OpCore():

    def pop(self, count=1, idx=-1):
        """( x -- )
        take something from the stack and return it"""
        try:
            return [self._stk.pop(idx) for i in range(count)]
        except IndexError as err:
            debug_write(err, "\n", level="RANGE")
            return None

    def push(self, *args, idx=-1):
        """( -- x )
        put somethings on the top of the stack"""
        if idx == -1:
            self._stk.extend(args)
        else:
            [self._stk.insert(idx, arg) for arg in args]

    def pick(self, idx=-1, upper_idx=-1):
        return self._stk[idx:upper_idx]

    def drop(self, count=1, idx=-1):
        [self._stk.pop(idx) for i in range(count)]

    def dup(self, count=1, idx=-1):
        y = self._stk[idx]
        [self._stk.append(y) for i in range(count)]

    def dup2(self, count=2, idx=-1):
        x, y = self._stk[idx], self._stk[idx-1]

class OpMath():
    pass

class OpString():
    pass

class Stack(OpCore, OpMath, OpString):

    def __init__(self):
        self._stk = []

