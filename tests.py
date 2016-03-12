#!/usr/bin/env python3

import forth
import unittest

from forth import cmp_all, is_none

from pmlr import pmlr

DEBUG = True

print     = pmlr.util.writer
dbg_write = pmlr.util.debug_write

class TestUtil(unittest.TestCase):

    def test_isnone(self):
        "none-tester"
        self.assertEqual(is_none(None), True)
        self.assertEqual(is_none("asd"), False)
        self.assertEqual(is_none(1, 2, 3, 4), False)
        self.assertEqual(is_none(1, 2, 3, None, 4), True)

    def test_cmpall(self):
        "cmp_all validation"
        self.assertEqual(cmp_all(3, 3), True)
        self.assertEqual(cmp_all(3, 4), False)
        self.assertEqual(cmp_all(4, None), False)
        self.assertEqual(cmp_all(3, 3, 4, 5), False)
        self.assertEqual(cmp_all(3, 3, 3, 3, 3), True)
        self.assertEqual(cmp_all(3, 4, 4, 4, 4), False)

class TestCoreOps(unittest.TestCase):

    def setUp(self):
        self.stk = forth.Stack()
        self.stk.push(1, 2, 3)

    def test_peek(self):
        "looking at the stack"
        try:
            assert self.stk.peek() == [1, 2, 3], \
                "stack peek failure, not continuing"
        except AssertionError as err:
            print(*err.args, "\nstack peek failure, not continuing", "\n")
            exit(127)

        self.assertEqual(self.stk.peek(), [1, 2, 3])

    def test_push(self):
        "pushing to the end"
        self.stk.push(1, 2, 3)
        self.assertEqual(self.stk.peek(), [1, 2, 3, 1, 2, 3])

    def test_push_toidx(self):
        "pushing to an index"
        self.stk.push(6, 7, idx=2)
        self.assertEqual(self.stk.peek(), [1, 2, 6, 7, 3])

    def test_push_to_negidx(self):
        "push to a negative index > 1"
        self.stk.push(7, 6, idx=-2)
        self.assertEqual(self.stk.peek(), [1, 6, 7, 2, 3])

    def test_pop(self):
        "take a value from the top"
        self.stk.pop()
        self.assertEqual(self.stk.peek(), [1, 2])

    def test_pop_returns(self):
        "take + ret the top value"
        self.assertEqual(self.stk.pop(), 3)

    def test_pop_multi(self):
        "get multiple (more than exist) items from TOS"
        self.stk.push(1, 2, 3, 4)
        s = self.stk.pop(55)
        self.assertEqual(s, [1, 2, 3, 1, 2, 3, 4])

    def test_clear(self):
        "completely clear all items"
        self.stk.clear()
        self.assertEqual(self.stk.peek(), [])

    def test_clear_returns(self):
        "clear all items and get them"
        s = self.stk.clear()
        self.stk.push(*s)
        self.assertEqual(self.stk.peek(), [1, 2, 3])

    def test_pick(self):
        "get an item from an index"
        self.assertEqual(self.stk.pick(), 3)

    def test_pick_range_lower(self):
        "get items from an index slice"
        self.assertEqual(self.stk.pick(lower=1), [2, 3])

    #def test_pick_range_upper(self):


if __name__ == '__main__':

    from sortUnittests import suiteFactory, caseFactory
    cases = suiteFactory(*caseFactory(scope = globals().copy()))

    runner = unittest.TextTestRunner(verbosity=2, failfast=True)
    runner.run(cases)
