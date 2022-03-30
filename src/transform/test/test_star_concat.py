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
        self.dfa2 = self.automatons['dfa2']

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
        concat_a = concat(self.dfa, self.dfa2)

        self.assertEqual(concat_a.initial_state, self.dfa.initial_state + "1")
        self.assertEqual(concat_a.terminal_states, ["A2"])
        self.assertEqual(concat_a.edges_epsilon, {'B1': ['A2'], 'C1': ['A2']})
        self.assertEqual(concat_a.states, ['A1', 'B1', 'C1', 'D1', 'E1', 'A2', 'B2'])
        self.assertEqual(concat_a.glossary, self.dfa.glossary)
        self.assertEqual(concat_a.edges, {'A1': [['C1', '1'], ['B1', '0'], ['A2', '1'], ['A2', '0']],
                                          'B1': [['D1', '1']], 'C1': [['E1', '1']],
                                          'D1': [['B1', '0'], ['C1', '1'], ['A2', '0'], ['A2', '1']],
                                          'E1': [['C1', '0'], ['A2', '0']],
                                          'A2': [['B2', '1']],
                                          'B2': [['A2', '0']]})
