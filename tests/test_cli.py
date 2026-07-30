import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from slugify_cli.cli import main


class TestCliText(unittest.TestCase):
    def test_slugifies_args(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["Hello, World!", "Café Society"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().splitlines(), ["hello-world", "cafe-society"])

    def test_reads_stdin_when_no_args(self) -> None:
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO("First Post!\nSecond One\n")):
            with redirect_stdout(out):
                code = main([])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().splitlines(), ["first-post", "second-one"])

    def test_custom_separator(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            main(["Hello World", "--separator", "_"])
        self.assertEqual(out.getvalue().strip(), "hello_world")


class TestCliRename(unittest.TestCase):
    def test_dry_run_does_not_rename(self) -> None:
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "Needs Fix.txt"
            f.write_text("x")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main(["--rename", tmp])
            self.assertEqual(code, 0)
            self.assertIn("Needs Fix.txt -> needs-fix.txt", out.getvalue())
            self.assertIn("Dry run", out.getvalue())
            self.assertTrue(f.exists())

    def test_apply_renames_file(self) -> None:
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "Needs Fix.txt"
            f.write_text("x")
            code = main(["--rename", tmp, "--apply"])
            self.assertEqual(code, 0)
            self.assertFalse(f.exists())
            self.assertTrue((Path(tmp) / "needs-fix.txt").exists())

    def test_nonexistent_directory_errors(self) -> None:
        code = main(["--rename", "/nonexistent/dir/for/sure"])
        self.assertEqual(code, 2)

    def test_no_changes_needed(self) -> None:
        with TemporaryDirectory() as tmp:
            (Path(tmp) / "already-good.txt").write_text("x")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main(["--rename", tmp])
            self.assertEqual(code, 0)
            self.assertIn("no filenames need changes", out.getvalue())


if __name__ == "__main__":
    unittest.main()
