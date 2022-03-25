import itertools

from src.automata import Automata
from src.minimize.minimize import minimize
from src.transform.transform import transform


def intersect_or_union(left: Automata, right: Automata, union: bool = False) -> Automata:
    if left.glossary != right.glossary:
        print("Glossaries of automatas are not equals")
        return left

    left = left if left.is_dfa else transform(left)
    right = right if right.is_dfa else transform(right)

    states = []
    terminal_states = []
    edges = {}

    for (left_state, right_state) in itertools.product(left.states, right.states):
        state = left_state + right_state
        states.append(state)
        left_in_terminal = left_state in left.terminal_states
        right_in_terminal = right_state in right.terminal_states

        if (union and (left_in_terminal or right_in_terminal)) or (left_in_terminal and right_in_terminal):
            terminal_states.append(state)

        edges[state] = [[left_edge_state + right_edge_state, left_edge_letter] for
                        ((left_edge_state, left_edge_letter), (right_edge_state, right_edge_letter)) in
                        itertools.product(left.edges[left_state], right.edges[right_state]) if
                        left_edge_letter == right_edge_letter]

    return minimize(Automata({
        'glossary': left.glossary,
        'states': states,
        'initial_state': left.initial_state + right.initial_state,
        'terminal_states': terminal_states,
        'is_dfa': True,
        'edges': edges,
        'edges_epsilon': {}
    }))
