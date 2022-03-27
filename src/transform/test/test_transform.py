import unittest
from src.main import save_automata
import src.reader.reader as automata_reader
from src.transform.transform import \
    __get_achievable_states as get_achievable_states, \
    to_dfa


class TestTransform(unittest.TestCase):
    def setUp(self) -> None:
        self.automatons = {}
        save_automata(
            self.automatons,
            automata_reader.read('src/test_data/test_data.json')
        )

        self.dfa = self.automatons['dfa']
        self.nfa = self.automatons['nfa']

    def test_achievable_states(self):
        self.assertEqual(['C', 'E'], sorted(get_achievable_states(self.nfa)))
        self.assertEqual(
            ['A', 'B', 'C', 'D', 'E'],
            sorted(get_achievable_states(self.dfa))
        )

    def test_to_dfa(self):
        dfa_ = to_dfa(self.nfa)
        self.assertTrue(dfa_.is_dfa)

        for v in dfa_.edges_epsilon.values():
            self.assertEqual(0, len(v))

        self.assertEqual(['C', 'E'], sorted(dfa_.states))
        self.assertEqual(['C'], dfa_.terminal_states)
        self.assertTrue(['E', '1'] in dfa_.edges['C'])
        self.assertTrue(['C', '0'] in dfa_.edges['E'])
