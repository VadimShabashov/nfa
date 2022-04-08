import unittest
import src.reader.reader as automata_reader
from src.check_word.check_word import check
from src.transform.transform import intersect_or_union, diff
from src.main import save_automata


class TestIntersectUnionDiff(unittest.TestCase):
    def setUp(self) -> None:
        self.automatons = {}
        save_automata(
            self.automatons,
            automata_reader.read('src/test_data/test_data.json')
        )

        self.nfa = self.automatons['nfa']
        self.dfa = self.automatons['dfa']
        self.dfa2 = self.automatons['dfa2']

    def test_intersect(self):
        automata = intersect_or_union(self.nfa, self.dfa)
        self.assertFalse(check(automata, "111"))
        self.assertFalse(check(automata, "11"))

    def test_union(self):
        automata = intersect_or_union(self.nfa, self.dfa, True)
        self.assertTrue(check(automata, "111"))
        self.assertTrue(check(automata, "11"))

    def test_diff(self):
        automata = self.nfa
        self.assertTrue(check(automata, "1010"))
        self.assertTrue(check(self.dfa2, "1010"))
        automata = diff(automata, self.dfa2)
        self.assertFalse(check(automata, "1010"))

    def test_diff_with_the_same(self):
        automata = self.nfa
        self.assertTrue(check(automata, "1010"))
        automata = diff(automata, self.nfa)
        self.assertFalse(check(automata, "1010"))
