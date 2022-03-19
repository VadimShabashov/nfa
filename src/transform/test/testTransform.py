import unittest
from src.automata import Automata
import src.reader.reader as automataReader
from src.transform.transform import \
    __get_achievable_states as get_achievable_states, \
    transform


class TestTransform(unittest.TestCase):
    def setUp(self) -> None:
        self.nfa = Automata(automataReader.read('src/examples/nfa1.txt'))
        self.dfa = Automata(automataReader.read('src/examples/dfa1.txt'))

    def test_achievable_states(self):
        self.assertEqual(['C', 'E'], sorted(get_achievable_states(self.nfa)))
        self.assertEqual(
            ['A', 'B', 'C', 'D', 'E'],
            sorted(get_achievable_states(self.dfa))
        )

    def test_transform(self):
        dfa_ = transform(self.nfa)
        self.assertTrue(dfa_.is_dfa)

        for v in dfa_.edges_epsilon.values():
            self.assertEqual(0, len(v))

        self.assertEqual(['C', 'E'], sorted(dfa_.states))
        self.assertEqual(['C'], dfa_.terminal_states)
        self.assertTrue(['E', '1'] in dfa_.edges['C'])
        self.assertTrue(['C', '0'] in dfa_.edges['E'])
