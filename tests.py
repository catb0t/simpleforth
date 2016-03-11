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
        self.assertEqual(is_none(None), True)
        self.assertEqual(is_none("asd"), False)
        self.assertEqual(is_none(1, 2, 3, 4), False)
        self.assertEqual(is_none(1, 2, 3, None, 4), True)

    def test_cmpall(self):
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
        try:
            assert self.stk.peek() == [1, 2, 3], \
                "stack peek failure, not continuing"
        except AssertionError as err:
            print(*err.args, "\nstack peek failure, not continuing", "\n")
            exit(127)

        self.assertEqual(self.stk.peek(), [1, 2, 3])

    def test_push(self):
        self.stk.push(1, 2, 3)
        self.assertEqual(self.stk.peek(), [1, 2, 3, 1, 2, 3])

    def test_pop(self):
        self.stk.pop()
        self.assertEqual(self.stk.peek(), [1, 2])

    def test_pop_returns(self):
        self.assertEqual(self.stk.pop(), 3)

    def test_pop_multi(self):
        self.stk.push(1, 2, 3, 4)
        s = self.stk.pop(55)
        self.assertEqual(s, [1, 2, 3, 1, 2, 3, 4])

    def test_clear(self):
        self.stk.clear()
        self.assertEqual(self.stk.peek(), [])

    def test_clear_returns(self):
        s = self.stk.clear()
        self.stk.push(*s)
        self.assertEqual(self.stk.peek(), [1, 2, 3])

    def test_pick(self):
        self.assertEqual(self.stk.pick(), 3)

    def test_pick_range(self):
        self.assertEqual(self.stk.pick(lower=1), [2, 3])


def suiteFactory(*testcases):

    ln    = lambda f: getattr(tc, f).__code__.co_firstlineno
    lncmp = lambda a, b: ln(a) - ln(b)

    test_suite = unittest.TestSuite()
    for tc in testcases:
        test_suite.addTest(unittest.makeSuite(tc, sortUsing=lncmp))

    return test_suite

def caseFactory():

    from inspect import findsource

    g = globals().copy()

    cases = [
        g[obj] for obj in g
            if obj.startswith("Test")
            and issubclass(g[obj], unittest.TestCase)
    ]

    ordered_cases = sorted(cases, key=lambda f: findsource(f)[1])

    return ordered_cases

if __name__ == '__main__':

    cases = suiteFactory(*caseFactory())
    runner = unittest.TextTestRunner(verbosity=2, failfast=False)
    runner.run(cases)

