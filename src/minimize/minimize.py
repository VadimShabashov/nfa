from src.automata import Automata
from collections import defaultdict
from src.minimize.classes_of_eq import DisjointSet


def minimize(automata: Automata):
    """
    DFA -> minDFA using standard table-filling method O(n^2)
    """
    dfa = delete_unreachable_states(automata)
    states = sorted(dfa.states)
    transitions = {}

    for k, v in dfa.edges.items():
        for i in v:
            transitions[(k, i[1])] = i[0]

    table = {}
    for i in states:
        for j in states:
            if i != j:
                if (i in dfa.terminal_states) != (j in dfa.terminal_states):
                    table[(i, j)] = True
                else:
                    table[(i, j)] = False

    flag = True

    while flag:
        flag = False

        for i in states:
            for j in states:
                if i != j:
                    if table[(i, j)]:
                        continue

                    for w in dfa.glossary:
                        path_1 = transitions.get((i, w), None)
                        path_2 = transitions.get((j, w), None)

                        if path_1 is not None and path_2 is not None:
                            if path_1 != path_2:
                                if path_1 < path_2:
                                    marked = table[(path_1, path_2)]
                                else:
                                    marked = table[(path_2, path_1)]
                                flag = flag or marked
                                table[(i, j)] = marked

                                if marked:
                                    break

    classes_of_eq = DisjointSet(dfa.states)

    for k, v in table.items():
        if not v:
            classes_of_eq.union(k[0], k[1])

    new_states = []
    for i in classes_of_eq.disjoint_set:
        new_states.append(",".join(i))

    dfa.states = new_states
    new_final_states = []
    dfa.initial_state = ",".join(classes_of_eq.find(dfa.initial_state))

    for s in classes_of_eq.get():
        for item in s:
            if item in dfa.terminal_states:
                new_final_states.append(",".join(classes_of_eq.find(item)))
                break

    new_transitons = {(",".join(classes_of_eq.find(k[0])), k[1]): ",".join(classes_of_eq.find(v))
                      for k, v in transitions.items()}
    new_edges = {}
    for k, v in new_transitons.items():
        if k[0] not in new_edges:
            new_edges[k[0]] = [[v, k[1]]]
        else:
            new_edges[k[0]].append([v, k[1]])

    dfa.edges = new_edges

    new_final_states = ["".join(i) for i in new_final_states]
    dfa.terminal_states = new_final_states

    return dfa


def delete_unreachable_states(automata):
    """
    Firstly, we remove states unreachable from start
    using DFS
    """
    graph = defaultdict(list)
    reachable_states = set()
    for k, v in automata.edges.items():
        for i in v:
            graph[k].append(i[0])

    stack = [automata.initial_state]
    while stack:
        state = stack.pop()
        if state not in reachable_states:
            stack += graph[state]
        reachable_states.add(state)

    new_states = [i for i in automata.states if i in reachable_states]
    automata.states = new_states
    new_terminal_states = [i for i in automata.terminal_states if i in reachable_states]
    automata.terminal_states = new_terminal_states
    new_edges = {k: v for k, v in automata.edges.items() if k in reachable_states}
    automata.edges = new_edges
    return automata
