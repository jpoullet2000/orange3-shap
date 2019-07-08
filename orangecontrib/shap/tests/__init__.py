import os
import unittest


def suite(loader=unittest.TestLoader(), pattern='test*.py'):
    all_tests = loader.discover(dir_, pattern, top_level_dir=top_level)
    return unittest.TestSuite(all_tests)


if __name__ == '__main__':
unittest.main(defaultTest='suite')