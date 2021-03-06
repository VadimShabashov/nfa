from src.automata import Automata
from src.transform.transform import to_dfa


def check(automata: Automata, word) -> bool:
    # для проверки слова будем использовать детерменированный автомат
    # если дали недетерменированный, сделаем трансформацию
    dfa = to_dfa(automata) if not automata.is_dfa else automata

    state = dfa.initial_state

    for char in word:
        found = False
        for edge in dfa.edges[state]:
            if edge[1] == char:
                state = edge[0]
                found = True
        if not found:
            print("Word is incorrect")
            return False

    if state in dfa.terminal_states:
        return True
    else:
        return False
