from copy import deepcopy
from collections import deque
import itertools
from typing import Dict, FrozenSet, List, Set, Tuple
from src.automata import Automata
from src.minimize.minimize import minimize


def concat(left: Automata, right: Automata) -> Automata:
    """
    this method is not completed yet
    """
    # if left.glossary != right.glossary:
    #     print("Glossaries of automatas are not equal")
    #     return left
    #
    # new_initial_state = left.initial_state
    # new_terminal_states = right.terminal_states
    # new_states = left.states.extend(right.states)
    #
    #
    # for k, v in left.edges.items():
    #     for i in v:
    raise NotImplementedError()



def star(a: Automata) -> Automata:
    new_initial_state = "Q1'"
    new_states = a.states.append(new_initial_state)
    new_edges = a.edges
    new_terminal_states = a.terminal_states.append(new_initial_state)

    for k, v in new_edges.items():
        if k in a.states:
            for i in v:
                if i[0] in a.terminal_states:
                    v.append([a.initial_state, i[1]])

    new_edges[new_initial_state] = edges[a.initial_state]

    a.initial_state = new_initial_state
    a.states = new_states
    a.terminal_states = new_terminal_states
    a.edges = new_edges

    return a


def diff(left: Automata, right: Automata) -> Automata:
    hell_state = '⊥'
    right.states.append(hell_state)
    right.edges[hell_state] = []
    new_terminal_states = [
        state
        for state
        in right.states
        if state not in right.terminal_states
    ]
    right.terminal_states = new_terminal_states
    for key in right.edges.keys():
        letters = [
            letter
            for letter
            in right.glossary
            if letter not in (map(lambda edge: edge[1], right.edges[key]))
        ]
        for letter in letters:
            right.edges[key].append([hell_state, letter])
    return intersect_or_union(left, right)


def intersect_or_union(left: Automata, right: Automata, union: bool = False)\
        -> Automata:
    if left.glossary != right.glossary:
        print("Glossaries of automatas are not equals")
        return left

    left = left if left.is_dfa else to_dfa(left)
    right = right if right.is_dfa else to_dfa(right)

    states = []
    terminal_states = []
    edges = {}

    for (left_state, right_state) in \
            itertools.product(left.states, right.states):
        state = left_state + right_state
        states.append(state)
        left_in_terminal = left_state in left.terminal_states
        right_in_terminal = right_state in right.terminal_states

        if (
            (union and (left_in_terminal or right_in_terminal))
            or (left_in_terminal and right_in_terminal)
        ):
            terminal_states.append(state)

        edges[state] = [
            [left_edge_state + right_edge_state, left_edge_letter]
            for (
                (left_edge_state, left_edge_letter),
                (right_edge_state, right_edge_letter)
            )
            in itertools.product(
                left.edges[left_state],
                right.edges[right_state]
            )
            if left_edge_letter == right_edge_letter
        ]

    return minimize(Automata({
        'glossary': left.glossary,
        'states': states,
        'initial_state': left.initial_state + right.initial_state,
        'terminal_states': terminal_states,
        'is_dfa': True,
        'edges': edges,
        'edges_epsilon': {}
    }))


def to_dfa(automata: Automata) -> Automata:
    without_epsilon = __remove_epsilon_edges(automata)
    raw_new_sigma: Dict[FrozenSet[str], List[Tuple[FrozenSet[str], str]]] = {}
    raw_new_states: Set[FrozenSet[str]] = set([
        frozenset([without_epsilon.initial_state])
    ])
    raw_new_terminals: Set[FrozenSet[str]] = set()
    queue = deque([frozenset(without_epsilon.initial_state)])

    while len(queue) > 0:
        s = queue.popleft()
        if s not in raw_new_sigma:
            raw_new_sigma[s] = []

        for char in without_epsilon.glossary:
            new_state = []
            terminal = False

            for original_state in s:
                if original_state in without_epsilon.terminal_states:
                    terminal = True

                for p in without_epsilon.edges[original_state]:
                    if p[1] == char:
                        new_state.append(p[0])

            if len(new_state) > 0:
                new_state = frozenset(new_state)
                raw_new_sigma[s].append((new_state, char))

                if terminal:
                    raw_new_terminals.add(s)

                if new_state not in raw_new_states:
                    raw_new_states.add(new_state)
                    queue.append(new_state)

    new_states = [__fs_to_str(s) for s in raw_new_states]

    return Automata({
        'glossary': without_epsilon.glossary,
        'states': new_states,
        'initial_state': without_epsilon.initial_state,
        'terminal_states': [__fs_to_str(s) for s in raw_new_terminals],
        'is_dfa': True,
        'edges': {
            __fs_to_str(k): [[__fs_to_str(p[0]), p[1]]for p in v]
            for (k, v) in raw_new_sigma.items()
        },
        'edges_epsilon': {state: [] for state in new_states}
    })


def __fs_to_str(fs: FrozenSet[str]) -> str:
    return "".join([str(e) + "-" for e in fs])[:-1]


def __get_achievable_states(a: Automata) -> List[str]:
    achievable_states = [a.initial_state]
    queue = deque([a.initial_state])

    while len(queue) > 0:
        s = queue.popleft()
        dests = [p[0] for p in a.edges[s]]

        for ds in dests:
            if ds not in achievable_states:
                achievable_states.append(ds)
                queue.append(ds)

    return achievable_states


def __get_epsilon_closure(a: Automata) -> Dict[str, List[str]]:
    epsilon_achievable = a.edges_epsilon
    mutated = True

    while mutated:
        mutated = False

        for (s, achievable) in epsilon_achievable.items():
            for ss in achievable:
                for sss in epsilon_achievable[ss]:
                    if sss not in achievable:
                        mutated = True
                        epsilon_achievable[s].append(sss)

    return epsilon_achievable


def __remove_epsilon_edges(a: Automata) -> Automata:
    achievable = __get_achievable_states(a)
    closure = __get_epsilon_closure(a)

    pre_automata = {
        'glossary': deepcopy(a.glossary),
        'states': achievable,
        'initial_state': a.initial_state,
        'terminal_states': [s for s in a.terminal_states if s in achievable],
        'is_dfa': a.is_dfa,
        'edges': {s: [] for s in achievable},
        'edges_epsilon': {}
    }

    for from_s in pre_automata['states']:
        for to_s in pre_automata['states']:
            for char in pre_automata['glossary']:
                if (
                    [to_s, char] in a.edges[from_s]
                    and [to_s, char] not in pre_automata['edges'][from_s]
                ):
                    pre_automata['edges'][from_s].append([to_s, char])
                else:
                    for ea in closure[from_s]:
                        if (
                            [to_s, char] in a.edges[ea]
                            and [to_s, char]
                                not in pre_automata['edges'][from_s]
                        ):
                            pre_automata['edges'][from_s].append([to_s, char])

    return Automata(pre_automata)
