from src.automata import Automata
from src.transform.transform import transform


def check(automata: Automata, word):
    # для проверки слова будем использовать детерменированный автомат
    # если дали недетерменированный, сделаем трансформацию
    dfa = transform(automata) if not automata.is_dfa else automata

    state = dfa.initial_state

    for char in word:
        found = False
        for edge in dfa.edges[state]:
            if edge[1] == char:
                state = edge[0]
                found = True
        if not found:
            print("Word is incorrect")
            return

    if state in dfa.terminal_states:
        print("Word is correct")
    else:
        print("Word is incorrect")
