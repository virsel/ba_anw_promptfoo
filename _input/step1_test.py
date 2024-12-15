from input.step1 import clean_pattern
import unittest


class TestCleanPattern(unittest.TestCase):
    def test_clean_pattern(self):
        test_case = "<:NUM:>:<:NUM:>:<:NUM:>.<:NUM:> INFO - TraceID: <:TRACEID:> SpanID: <:SPANID:> Received ad request (context words=<:ITEM:>"
        expected = "INFO - Received ad request context"
        self.assertEqual(clean_pattern(test_case), expected)

def main():
    unittest.main()

if __name__ == '__main__':
    main()