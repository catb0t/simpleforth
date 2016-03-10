#!/usr/bin/env python3

import builtins

from pmlr import pmlr

debug_write = pmlr.util.debug_write

ERR_DATA = {
    ZeroDivisionError:  {"IS_FATAL": False, "TYPE": "DEBUG"},
    LookupError:        {"IS_FATAL": False, "TYPE": "RANGE"},
    IndexError:         {"IS_FATAL": False, "TYPE": "RANGE"},
    TypeError:          {"IS_FATAL": True,  "TYPE": "ERROR"},
    NameError:          {"IS_FATAL": True,  "TYPE": "FATAL"},
    ValueError:         {"IS_FATAL": True,  "TYPE": "FATAL"},
    AssertionError:     {"IS_FATAL": True,  "TYPE": "FATAL"},
}


def is_none(*args):
    return None in args


def cmp_all(val, *tests):
    return builtins.all([val == test for test in tests])


def all(*args):
    return builtins.all(args)


def any(*args):
    return builtins.any(args)


class Forth(object):

    def __init__(self):
        (self._stk, self._lopstk,
            self._retstk, self._sftstk) = [Stack() for i in range(4)]

        self.dict = {
            "": ()
        }

        self.funcdict = {
            "": ()
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

    """bare stack operator mixin"""

    def peek(self, from_idx=0, to_idx=-1):
        return self._stk[:]

    def pop(self, count=1, idx=-1):
        """( x -- )
        take something and return it"""
        if count > len(self._stk):
            pmlr.util.debug_write(
                "popping more items than exist on stack!\n",
                level="WARN"
            )

        # http://stackoverflow.com/a/34633242/4532996
        # pop(x) is slower than pop()
        # pop(-1) doesn't seem to be optimised to pop(),
        # so avoid it if possible

        x = []
        if -1 == idx:
            for i in range(count):
                try:
                    x.append(self._stk.pop())
                except LookupError as err:
                    self.err(err, errtype="RANGE")
                    break
        else:
            for i in range(count):
                try:
                    x.append(self._stk.pop(idx))
                except LookupError as err:
                    self.err(err, errtype="RANGE")
                    break

        return x[0] if len(x) == 1 else x

    def push(self, *args, idx=-1):
        """( -- x ... )
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

    def pick(self, lower=-1, upper=-1):
        """( x -- x )
        pick somethings from a range of indicies"""

        if cmp_all(-1, lower, upper) or all(lower == -1, upper == 0):
            return self._stk[-1]

        # "string"[0:-1] == "strin"
        elif all(lower == 0, upper == -1):
            return self._stk[:]

        elif upper == -1:
            return self._stk[lower:]

        else:
            try:
                s = self._stk[lower:upper]
                assert bool(s) == bool(self._stk), \
                    (
                        pmlr.util.debug_fmt("FATAL")
                        + " pick returned result inconsistent with stack state"
                    )

            # special cases of these exceptions: we want to rethrow
            # because they should be exceptional circumstances
            except LookupError as err:
                self.err(err, errtype="RANGE")
                raise
                return None

            except AssertionError as err:
                self.err(err, errtype="FATAL")
                raise
                return None
            else:
                return s[0] if len(s) == 1 else s

    def drop(self, count=1, idx=-1):
        """( x -- )
        drop items without returning (cheaper pop)"""
        [self.pop(idx=idx) for i in range(count)]

    def dup(self, count=1, from_idx=-1):
        """( y -- y y )
        duplicate something and push"""
        try:
            y = self._stk[from_idx] * count
        except LookupError as err:
            self.err(err, errtype="RANGE")

        self.push(*y, idx=idx)

    def dupn(self, count=2, idx=-1):
        """( x y -- x y x y )
        dup count items from an idx"""
        y = []
        for i in range(count):
            try:
                y.append(self._stk[idx - i])
            except LookupError as err:
                if idx == 1:
                    continue
                else:
                    self.err(err, errtype="RANGE")
                    return None

        self._stk.extend(y)

    def swap(self, idx=-1):
        """( x y -- y x )
        swap two things at an index"""
        self.push(*reversed([self.pop(idx=idx) for i in range(2)]), idx=idx)

    def rot(self, idx=-1, count=3):
        """( w x y z -- x y z w )
        rotate things left, at an index"""
        l = [self.pop(idx=idx) for i in range(count)]
        l.insert(0, l.pop())
        self.push(*l, idx=idx)

    def urot(self, idx=-1, count=3):
        """( w x y z -- z w x y )
        rotate things right, at an index"""
        l = [self.pop(idx=idx) for i in range(count)]
        l.append(l.pop(0))
        self.push(*l, idx=idx)


class OpLogik():
    pass

class OpString():
    pass


class Stack(OpCore, OpLogik, OpString):

    "the mixin mixer of the above mixins"

    def __init__(self):
        self._stk = []

    def err(self, err, errtype=None, framelevel=3):
        if errtype is None:
            errtype = ERR_DATA.get(err.__class__, {"TYPE": "FATAL"})["TYPE"]

        errtype = errtype.upper()

        debug_write(*err.args, "\n", level=errtype, framelevel=framelevel)

        if ERR_DATA.get(err.__class__, {"IS_FATAL": True})["IS_FATAL"]:
            raise err.__class__(
                pmlr.util.debug_fmt(
                    errtype, framelevel=framelevel
                ) + " " + "".join(*err.args)
            )
