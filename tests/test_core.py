import unittest

from slugify_cli.core import plan_renames, slugify, slugify_filename


class TestSlugify(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_collapses_repeated_punctuation(self) -> None:
        self.assertEqual(slugify("Café  Society"), "cafe-society")

    def test_strips_accents(self) -> None:
        self.assertEqual(slugify("Élan Vital"), "elan-vital")

    def test_strips_leading_trailing_punctuation(self) -> None:
        self.assertEqual(slugify("  -- neat! --  "), "neat")

    def test_custom_separator(self) -> None:
        self.assertEqual(slugify("Hello World", separator="_"), "hello_world")

    def test_empty_string(self) -> None:
        self.assertEqual(slugify(""), "")

    def test_numbers_preserved(self) -> None:
        self.assertEqual(slugify("Top 10 Tips"), "top-10-tips")


class TestSlugifyFilename(unittest.TestCase):
    def test_preserves_and_lowercases_extension(self) -> None:
        self.assertEqual(slugify_filename("My Report (Final).PDF"), "my-report-final.pdf")

    def test_no_extension(self) -> None:
        self.assertEqual(slugify_filename("README"), "readme")

    def test_empty_stem_falls_back(self) -> None:
        self.assertEqual(slugify_filename("!!!.txt"), "file.txt")


class TestPlanRenames(unittest.TestCase):
    def test_only_includes_changed_names(self) -> None:
        renames = plan_renames(["already-good.txt", "Needs Fix.txt"])
        self.assertEqual(renames, [("Needs Fix.txt", "needs-fix.txt")])

    def test_avoids_collisions(self) -> None:
        renames = plan_renames(["Report!.txt", "Report?.txt"])
        new_names = [n for _, n in renames]
        self.assertEqual(len(new_names), len(set(new_names)))
        self.assertIn("report.txt", new_names)
        self.assertIn("report-2.txt", new_names)

    def test_avoids_collision_with_untouched_existing_file(self) -> None:
        renames = plan_renames(["report.txt", "Report!.txt"])
        # "report.txt" is untouched (already a valid slug); "Report!.txt"
        # must not be renamed onto it.
        targets = dict(renames)
        self.assertEqual(targets["Report!.txt"], "report-2.txt")


if __name__ == "__main__":
    unittest.main()
