def check_duplicates(lst):
    set_lst = set()
    set_duplicates = set()
    for item in lst:
        if item in set_lst:
            set_duplicates.add(item)
        else:
            set_lst.add(item)

    return set_duplicates, set_lst


def check_keys_match(test_set, correct_set):
    extra_fields = test_set.difference(correct_set)
    required_fields = correct_set.difference(test_set)
    return extra_fields, required_fields


def check_keys_subset(test_set, correct_set):
    diff_set = test_set.difference(correct_set)
    return diff_set


def check_automata(data):
    status = []

    # Проверка общих полей в данных
    correct_keys = {"glossary", "states", "initial_state", "terminal_states", "is_dfa", "edges", "edges_epsilon"}
    extra_keys, required_keys = check_keys_match(set(data.keys()), correct_keys)
    if extra_keys or required_keys:
        return f"Wrong fields in data: unknown fields {extra_keys}, missing fields {required_keys}"

    # Проверка всех состояний
    states_duplicates, states = check_duplicates(data["states"])
    if states_duplicates:
        status.append(f"Duplication of states for {states_duplicates}")

    # Проверка, начального состояния
    if data["initial_state"] not in states:
        status.append(f"Initial state {data['initial_state']} is not in states")

    # Проверка терминальных состояний
    terminal_states_duplicates, terminal_states = check_duplicates(data["terminal_states"])
    if terminal_states_duplicates:
        status.append(f"Duplication of terminal states for {terminal_states_duplicates}")
    diff_terminal_states = check_keys_subset(terminal_states, states)
    if diff_terminal_states:
        status.append(f"States {diff_terminal_states} of terminal states are not in states")

    # Проверка словаря
    glossary_duplicates, glossary = check_duplicates(data["glossary"])
    if glossary_duplicates:
        status.append(f"Duplication of symbols in glossary for {glossary_duplicates}")

    # Проверка НЕ эпсилон ребер
    extra_keys_edges, required_keys_edges = check_keys_match(set(data["edges"].keys()), states)
    if extra_keys_edges or required_keys_edges:
        status.append(f"Set of edges keys doesn't equal set of states: "
                      f"unknown fields {extra_keys_edges}, missing fields {required_keys_edges}")
    for start_state, edges in data["edges"].items():
        set_edges = set()
        set_symbols = set()
        for end_state, edge in edges:
            if end_state not in states:
                status.append(f"State {end_state} in edges (for {start_state}: ({end_state}, {edge})) is not in states")
            if edge not in glossary:
                status.append(f"Edge {edge} in edges (for {start_state}: ({end_state}, {edge})) is not in glossary")
            if (end_state, edge) in set_edges:
                status.append(f"Duplication of edge {start_state}: ({end_state}, {edge}) in edges")
            else:
                set_edges.add((end_state, edge))
            if data["is_dfa"] and (edge in set_symbols):
                status.append(f"Multiple edges '{edge}' were specified for {start_state} in DFA.")
            else:
                set_symbols.add(edge)

    # Проверка эпсилон ребер
    extra_keys_epsilon_edges, required_keys_epsilon_edges = check_keys_match(set(data["edges_epsilon"].keys()), states)
    if extra_keys_epsilon_edges or required_keys_epsilon_edges:
        status.append(f"Set of epsilon edges keys doesn't equal set of states: "
                      f"unknown keys {extra_keys_epsilon_edges}, missing keys {required_keys_epsilon_edges}")
    for start_state, edges in data["edges_epsilon"].items():
        if data["is_dfa"] and edges:
            status.append(f"Epsilon edges can not be specified for DFA.")
            break
        else:
            edges_duplicate, set_edges = check_duplicates(edges)
            if edges_duplicate:
                status.append(f"Duplication of epsilon edges for {start_state}: {edges_duplicate}")
            diff_epsilon_edges = check_keys_subset(set_edges, states)
            if diff_epsilon_edges:
                status.append(f"States {diff_epsilon_edges} for {start_state} in epsilon edges are not in states")

    return "\n".join(status)
