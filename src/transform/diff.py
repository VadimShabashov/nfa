from src.automata import Automata
from src.transform.intersect_or_union import intersect_or_union


def diff(left: Automata, right: Automata) -> Automata:
    hell_state = '⊥'
    right.states.append(hell_state)
    new_terminal_states = [state for state in right.states if state not in right.terminal_states]
    right.terminal_states = new_terminal_states
    for key in right.edges.keys():
        for letter in right.glossary:
            right.edges[key].append([hell_state, letter])
    return intersect_or_union(left, right)
