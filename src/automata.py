from typing import Dict, List


class Automata:
    def __init__(self, data):
        self.glossary: List[str] = data["glossary"]
        self.states: List[str] = data["states"]
        self.initial_state: str = data["initial_state"]
        self.terminal_states: List[str] = data["terminal_states"]
        self.edges: Dict[str, List[List[str]]] = data["edges"]
        self.edges_epsilon: Dict[str, List[str]] = data["edges_epsilon"]
        self.is_dfa: bool = data["is_dfa"]

    def __repr__(self):
        return 'Automata({\n' \
            f'  "glossary": {repr(self.glossary)},\n' \
            f'  "states": {repr(self.states)},\n' \
            f'  "initial_state": {repr(self.initial_state)},\n' \
            f'  "terminal_states": {repr(self.terminal_states)},\n' \
            f'  "edges: {repr(self.edges)},\n' \
            f'  "edges_epsilon": {repr(self.edges_epsilon)},\n' \
            f'  "is_dfa": {repr(self.is_dfa)}\n' \
            '})'
