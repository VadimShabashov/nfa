from copy import deepcopy
from collections import deque
from typing import Dict, FrozenSet, List, Set, Tuple
from src.automata import Automata


def transform(automata: Automata) -> Automata:
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
