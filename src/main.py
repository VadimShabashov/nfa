import sys
import json
from reader.reader import read
from writer.writer import write
from data_validation.data_validation import check_automata
from visualization.visualization import visualize


class NFA:
    def __init__(self, data):
        self.glossary = data["glossary"]
        self.states = data["states"]
        self.initial_state = data["initial_state"]
        self.terminal_states = data["terminal_states"]
        self.edges = data["edges"]
        self.edges_epsilon = data["edges_epsilon"]
        self.is_dfa = data["is_dfa"]


def check_args(args):
    if len(args) != 1:
        print(f"Wrong number of arguments were provided: expected 1, got {len(args)}")
        return 0
    else:
        return 1


def execute_command(automata, command, *args):
    if command not in ["read", "visualize", "minimize", "transform", "check", "write"]:
        print(f"Unknown command: {command}")
        return automata

    try:
        if command == "read":
            if check_args(args):
                try:
                    data = read(*args)
                    data_status = check_automata(data)
                    if not data_status:
                        automata = NFA(data)
                        print("Read automata successfully")
                    else:
                        print("Following problems in data were found:\n" + data_status)
                except FileNotFoundError:
                    print(f"File wasn't found.")
                except json.JSONDecodeError as e:
                    print(f"JSON error: {e.msg}")
            return automata

        if automata:
            if command == "minimize":
                if automata.is_dfa:
                    automata = minimize(automata)
                else:
                    print(f"Can't minimize NFA. Please, transform it first to the DFA.")
            elif command == "transform":
                automata = transform(automata)
            elif command == "visualize":
                visualize(automata)
            elif command == "check":
                if check_args(args):
                    check(automata, *args)
            else:
                if check_args(args):
                    try:
                        write(automata, *args)
                        print("Wrote successfully")
                    except FileNotFoundError:
                        print("Can't open output file!")
        else:
            print(f"No automata was provided yet for command {command}")

        return automata

    except Exception as e:
        print(f"Unexpected error: {e}")
        return automata


def run_nfa():
    """
    Реализуем REPL. Читаем из командной строки и вызываем соответствующую функцию.
    """
    automata = None
    while True:
        command_args = sys.stdin.readline().split()

        if command_args:
            if command_args == ["exit"]:
                break
            else:
                automata = execute_command(automata, *command_args)


if __name__ == "__main__":
    print("App is started. Welcome, sir/madame!")
    run_nfa()
    print("App is terminated. Good day, sir/madame!")