import unittest
import src.reader.reader as automataReader
from src.data_validation.data_validation import validate


class TestValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.automatons = automataReader.read('src/test_data/test_data.json')
        self.wrong = automataReader.read(
            'src/data_validation/test/test_data/wrong.json'
        )
        self.with_cycle = automataReader.read(
            'src/data_validation/test/test_data/with_cycle.json'
        )

    def test_validator(self):
        self.assertIsNone(validate(self.automatons))

        r = validate(self.wrong)
        self.assertIsNotNone(r)
        r = r.split('\n')
        self.assertEqual(3, len(r))
        self.assertIn('Name name4 not presented in file', r)
        self.assertIn(
            'Only one operator per automata allowed. '
            'Please separate operations into multiple automatons',
            r
        )

        r = validate(self.with_cycle)
        self.assertIsNotNone(validate(self.with_cycle))
        r = r.split('\n')
        self.assertEqual(1, len(r))
        self.assertIn('Cycle dependency found', r)
