import unittest

from src.main import parse_command


class TestStage1(unittest.TestCase):

    def test_simple_command(self):
        self.assertEqual(
            parse_command("ls file.txt"),
            ["ls", "file.txt"]
        )

    def test_quoted_argument(self):
        self.assertEqual(
            parse_command('cd "my folder"'),
            ["cd", "my folder"]
        )

    def test_multiple_arguments(self):
        self.assertEqual(
            parse_command("ls file1 file2"),
            ["ls", "file1", "file2"]
        )

    def test_invalid_quotes(self):
        with self.assertRaises(ValueError):
            parse_command('cd "my folder')


if __name__ == "__main__":
    unittest.main()
