import unittest
import src.reader.reader as automataReader
from src.data_validation.data_validation import validate


class TestValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.nfa = automataReader.read('src/examples/nfa1.json')
        self.dfa = automataReader.read('src/examples/dfa1.json')
        self.wrong = automataReader.read('src/data_validation/test/wrong.json')
        self.with_cycle = automataReader.read(
            'src/data_validation/test/with_cycle.json'
        )

    def test_validator(self):
        self.assertIsNone(validate(self.dfa))
        self.assertIsNone(validate(self.nfa))

        r = validate(self.wrong)
        self.assertIsNotNone(r)
        r = r.split('\n')
        self.assertEqual(3, len(r))
        self.assertIn('Name name4 not presented in file', r)
        self.assertIn('name and name3 cannot follow in sequence', r)

        r = validate(self.with_cycle)
        self.assertIsNotNone(validate(self.with_cycle))
        r = r.split('\n')
        self.assertEqual(1, len(r))
        self.assertIn('Cycle dependency found', r)
