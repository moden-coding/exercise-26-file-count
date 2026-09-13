#!/usr/bin/env python3

import contextlib
import io
import sys
import unittest
from unittest.mock import patch
from itertools import repeat

from src.file_count import file_count, main


class FileCount(unittest.TestCase):

    def test_first(self):
        l, w, c = file_count("src/test.txt")
        self.assertEqual(
            l, 8,
            msg="file_count('src/test.txt') should report 8 lines. Got %r."
            % (l,))
        self.assertEqual(
            w, 105,
            msg="file_count('src/test.txt') should report 105 words. "
            "Got %r." % (w,))
        self.assertEqual(
            c, 647,
            msg="file_count('src/test.txt') should report 647 characters. "
            "Got %r." % (c,))

    def test_calls(self):
        with patch('builtins.open', side_effect=open) as o:
            file_count("src/test.txt")
            o.assert_called_once()

    def test_main(self):
        orig_argv = sys.argv
        n = 7
        sys.argv[1:] = ["file%i" % i for i in range(n)]
        try:
            with patch('src.file_count.file_count',
                       side_effect=repeat((0, 0, 0))) as fc:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    main()
                self.assertEqual(
                    fc.call_count, n,
                    msg="main() should call file_count() once per command "
                    "line argument (expected %i calls for %i arguments)."
                    % (n, n))
            result = buf.getvalue().strip().split('\n')
            for i, line in enumerate(result):
                self.assertEqual(
                    line.strip(), "0\t0\t0\tfile%i" % i,
                    msg="main() printed the wrong line for file%i when "
                    "file_count() returns (0, 0, 0)." % i)
        finally:
            sys.argv = orig_argv


if __name__ == '__main__':
    unittest.main()
