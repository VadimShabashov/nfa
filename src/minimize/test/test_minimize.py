import unittest
import src.reader.reader as automata_reader
from src.minimize.minimize import minimize
from src.main import save_automata


class TestMinimize(unittest.TestCase):
    def setUp(self):
        self.automatons = {}
        save_automata(
            self.automatons,
            automata_reader.read('src/test_data/test_data.json')
        )

        self.dfa = self.automatons['dfa']
        self.minDFA = minimize(self.dfa)

    def test_minimize(self):
        self.assertEqual('A,D,E', self.minDFA.initial_state)
        self.assertEqual(['A,D,E', 'B,C'], sorted(self.minDFA.states))
        self.assertEqual(self.dfa.edges_epsilon, self.minDFA.edges_epsilon)
        self.assertEqual(self.dfa.glossary, self.minDFA.glossary)
        self.assertEqual(
            {
                'A,D,E': [['B,C', '1'], ['B,C', '0']],
                'B,C': [['A,D,E', '1']]
            },
            self.minDFA.edges
        )
        self.assertTrue(self.minDFA.is_dfa)
        self.assertEqual(['B,C'], sorted(self.minDFA.terminal_states))
