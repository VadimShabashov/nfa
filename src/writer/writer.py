import json


def write(automata, file_name):
    data = {"glossary": automata.glossary,
            "states": automata.states,
            "initial_states": automata.initial_state,
            "terminal_states": automata.terminal_states,
            "is_dfa": automata.is_dfa,
            "edges": automata.edges,
            "edges_epsilon": automata.edges_epsilon}

    try:
        with open(file_name, '+w') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=2)
    except Exception:
        raise
