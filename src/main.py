import sys
import json
from reader.reader import read
from check_word.check_word import check
from minimize.minimize import minimize
from src.automata import Automata
from src.transform.diff import diff
from src.transform.intersect_or_union import intersect_or_union
from transform.transform import transform
from writer.writer import write
from data_validation.data_validation import check_automata
from visualization.visualization import visualize


def check_args(args):
    if len(args) != 1:
        print(f"Wrong number of arguments were provided: expected 1, got {len(args)}")
        return False
    else:
        return True


def read_automata(args, default_automata):
    automata = default_automata
    if check_args(args):
        try:
            data = read(*args)
            data_status = check_automata(data)
            if not data_status:
                automata = Automata(data)
                print("Read automata successfully")
            else:
                print("Following problems in data were found:\n" + data_status)
        except FileNotFoundError:
            print(f"File wasn't found.")
        except json.JSONDecodeError as e:
            print(f"JSON error: {e.msg}")
    return automata


def execute_command(automata, command, *args):
    if command not in ["read", "visualize", "minimize", "transform", "check", "write", "union", "intersect", "diff"]:
        print(f"Unknown command: {command}")
        return automata

    try:
        if command == "read":
            return read_automata(args, automata)

        if automata:
            if command == "minimize":
                if automata.is_dfa:
                    automata = minimize(automata)
                    print("Minimized automata successfully")
                else:
                    print(f"Can't minimize NFA. Please, transform it first to the DFA.")
            elif command == "transform":
                automata = transform(automata)
                print("Transformed automata successfully")
            elif command == "visualize":
                visualize(automata)
            elif command == "check":
                if check_args(args):
                    check(automata, *args)
            elif command == "union":
                if check_args(args):
                    with_automata = read_automata(args, automata)
                    if with_automata != automata:
                        return intersect_or_union(automata, with_automata, True)
            elif command == "intersect":
                if check_args(args):
                    with_automata = read_automata(args, automata)
                    if with_automata != automata:
                        return intersect_or_union(automata, with_automata)
            elif command == "diff":
                if check_args(args):
                    with_automata = read_automata(args, automata)
                    if with_automata != automata:
                        return diff(automata, with_automata)
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
