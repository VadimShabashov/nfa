import unittest
from src.automata import Automata
import src.reader.reader as automata_reader
from src.check_word.check_word import check
from src.transform.diff import diff
from src.transform.intersect_or_union import intersect_or_union


class TestIntersectUnionDiff(unittest.TestCase):
    def setUp(self) -> None:
        self.nfa = Automata(automata_reader.read('src/examples/nfa1.txt'))
        self.dfa = Automata(automata_reader.read('src/examples/dfa1.txt'))
        self.dfa2 = Automata(automata_reader.read('src/examples/dfa2.txt'))

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

