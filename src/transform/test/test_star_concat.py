import unittest
import src.reader.reader as automata_reader
from src.main import save_automata
from src.transform.transform import star, concat


class TestStarConcat(unittest.TestCase):
    def setUp(self) -> None:
        self.automatons = {}
        save_automata(
            self.automatons,
            automata_reader.read('src/test_data/test_data.json')
        )

        self.dfa = self.automatons['dfa']
        self.nfa = self.automatons['nfa']

    def test_star(self):
        iter_automata = star(self.dfa)

        self.assertEqual(iter_automata.glossary, self.dfa.glossary)
        self.assertEqual(iter_automata.initial_state, "A'")
        self.assertEqual(iter_automata.states, ['A', 'B', 'C', 'D', 'E', "A'"])
        self.assertEqual(iter_automata.terminal_states, ['B', 'C', "A'"])
        self.assertEqual(iter_automata.edges, {'A': [['C', '1'], ['B', '0'], ['A', '1'],
                                                     ['A', '0']], 'B': [['D', '1']], 'C': [['E', '1']],
                                               'D': [['B', '0'], ['C', '1'], ['A', '0'], ['A', '1']],
                                               'E': [['C', '0'], ['A', '0']],
                                               "A'": [['C', '1'], ['B', '0'], ['A', '1'], ['A', '0']]})

    def test_concat(self):
        pass