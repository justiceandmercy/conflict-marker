import os
import tempfile
import unittest

from scanner import scan_file, scan_dir, _is_marker


class TestMarker(unittest.TestCase):
    def test_is_marker(self):
        self.assertTrue(_is_marker("<<<<<<< HEAD\n"))
        self.assertTrue(_is_marker("=======\n"))
        self.assertTrue(_is_marker(">>>>>>> branch\n"))
        self.assertFalse(_is_marker("hello world\n"))

    def test_scan_file(self):
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        with open(path, "w") as f:
            f.write("line1\n<<<<<<< HEAD\n=======\n>>>>>>> b\nend\n")
        try:
            res = scan_file(path)
            self.assertEqual(len(res), 3)
        finally:
            os.remove(path)

    def test_scan_dir_ignores_git(self):
        d = tempfile.mkdtemp()
        with open(os.path.join(d, "a.py"), "w") as f:
            f.write("x = 1\n<<<<<<< HEAD\n")
        with open(os.path.join(d, "clean.py"), "w") as f:
            f.write("y = 2\n")
        gitdir = os.path.join(d, ".git")
        os.makedirs(gitdir)
        with open(os.path.join(gitdir, "x"), "w") as f:
            f.write("<<<<<<< HEAD\n")
        res = scan_dir(d)
        self.assertEqual(len(res), 1)

    def test_extension_filter(self):
        d = tempfile.mkdtemp()
        with open(os.path.join(d, "a.py"), "w") as f:
            f.write("<<<<<<< HEAD\n")
        with open(os.path.join(d, "b.js"), "w") as f:
            f.write("<<<<<<< HEAD\n")
        res = scan_dir(d, extensions=[".py"])
        self.assertEqual(len(res), 1)


if __name__ == "__main__":
    unittest.main()
