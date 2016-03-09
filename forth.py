#!/usr/bin/env python3

from pmlr import pmlr

debug_write = pmlr.util.debug_write

IS_FATAL = {
    ZeroDivisionError:  {"IS_FATAL": False, "TYPE": "DEBUG"},
    IndexError:         {"IS_FATAL": False, "TYPE": "RANGE"},
    NameError:          {"IS_FATAL": True,  "TYPE": "FATAL"},
    TypeError:          {"IS_FATAL": True,  "TYPE": "FATAL"},
    ValueError:         {"IS_FATAL": True,  "TYPE": "FATAL"},
}


def is_none(*args):
    return True if None in args else False


class MalformedExpressionException(Warning):

    def __init__(self, *msg, level="INFO"):
        self.msg = msg
        self.level = level

    def __str__(self):
        return msg

    def __repr__(self):
        return self.__str__()

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
            debug_write(err.msg, level=err.level)

        return None  # {"name": "None", "desc": "debug"}


class OpCore():

    """bare stackman ops"""

    def pop(self, count=1, idx=-1):
        """( x -- )
        take something and return it"""
        try:
            # http://stackoverflow.com/a/34633242/4532996
            # pop(x) is slower than pop()
            # pop(-1) doesn't seem to be optimised to pop(),
            # so avoid it if possible
            if idx == -1:
                return [self._stk.pop()] * count
            else:
                return [self._stk.pop(idx)] * count

        except IndexError as err:
            self.dbg_range(err)
            return None

    def push(self, *args, idx=-1):
        """( -- x )
        put somethings at idx"""
        if idx == -1:
            self._stk.extend(args)
        else:
            [self._stk.insert(idx, arg) for arg in args]


    def clear(self):
        """( z y x -- )
        clear the stack completely"""
        y = self._stk.copy()
        self._stk.clear()
        return y

    def pick(self, idx=-1, upper_idx=-1):
        """( z y x -- z x )
        pick somethings from a range of indicies"""
        try:
            return self._stk[idx:upper_idx]
        except IndexError as err:
            self.dbg_range(err)
            return None

    def drop(self, count=1, idx=-1):
        """( x -- )
        drop items without returning (cheaper pop)"""
        [self.pop(idx=idx)] * count

    def dup(self, count=1, from_idx=-1):
        """( y -- y y )
        duplicate something and push"""
        try:
            y = self._stk[from_idx] * count
        except IndexError as err:
            self.dbg_range(err)

        self.push(*y, idx=idx)

    def dupn(self, count=2, idx=-1):
        """( x y -- x y x y )
        dup count items from an idx"""
        y = []
        for i in range(count):
            try:
                y.append(self._stk[idx - i])
            except IndexError as err:
                if idx == 1:
                    continue
                else:
                    self.dbg_range(err)
                    return None

        self._stk.extend(y)

    def swap(self, idx=-1):
        """( x y -- y x )
        swap two things at an index"""
        self.push(*reversed([self.pop(idx=idx)] * 2), idx=idx)

    def rot(self, idx=-1, count=3):
        """( w x y z -- x y z w )
        rotate things left, at an index"""
        l = [self.pop(idx=idx)] * count
        l.insert(0, l.pop())
        self.push(*l, idx=idx)

    def urot(self, idx=-1, count=3):
        """( w x y z -- z w x y )
        rotate things right, at an index"""

class OpMath():
    pass


class OpString():
    pass


class Stack(OpCore, OpMath, OpString):

    def __init__(self):
        self._stk = []

    def err(self, err, errtype=None):
        if errtype is None:
            errtype = ERR_DATA.get(err.__class__, {"TYPE": "FATAL"})["TYPE"]

        errtype = errtype.upper()

        debug_write(*err.args, "\n", level=errtype)

        if ERR_DATA.get(err.__class__, {"IS_FATAL": True})["IS_FATAL"]:
            raise err.__class__(pmlr.debug_fmt(errtype) + " :: ".join(*err.args))
