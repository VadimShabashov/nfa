import json
from src.reader.reader import read
from src.check_word.check_word import check
from src.minimize.minimize import minimize
from src.automata import Automata
from src.transform.transform import to_dfa
from src.writer.writer import write
from src.data_validation.data_validation import validate
from src.visualization.visualization import visualize
from src.apply_operations.apply_operations import apply_operations


def check_args(args):
    if len(args) != 1:
        print(f"Wrong number of arguments were provided: expected 1, got {len(args)}")
        return False
    else:
        return True


def save_automata(dict_automata, data):
    for automata_name, body in data.items():
        if isinstance(body, dict):
            dict_automata[automata_name] = Automata(body)
        else:
            apply_operations(dict_automata, automata_name, body)


def read_automata(dict_automata, *args):
    if check_args(args):
        try:
            data = read(*args)
            data_status = validate(data)
            if not data_status:
                save_automata(dict_automata, data)
                print("Read automata successfully")
            else:
                print("Following problems in data were found:\n" + data_status)
        except FileNotFoundError:
            print(f"File wasn't found.")
        except json.JSONDecodeError as e:
            print(f"JSON error: {e.msg}")


def execute_command(dict_automata, *args):
    if len(args) == 0:
        print(f"Empty string was given instead of a command")
    elif args[0] in ["read", "visualize", "minimize", "transform", "check", "write"]:
        command = args[0]
        command_args = args[1:]
        try:
            if command == "read":
                read_automata(dict_automata, *command_args)
            elif len(command_args) < 1:
                print(f"Not enough arguments were provided for command {command}")
            else:
                automata_name = command_args[0]
                arguments = command_args[1:]
                if automata_name not in dict_automata:
                    print(f"Unknown automata with name '{automata_name}' was provided for command '{command}'")
                else:
                    automata = dict_automata[automata_name]
                    if command == "minimize":
                        if automata.is_dfa:
                            dict_automata[automata_name] = minimize(automata)
                            print("Minimized automata successfully")
                        else:
                            print(f"Can't minimize NFA. Please, transform it first to the DFA.")
                    elif command == "transform":
                        dict_automata[automata_name] = to_dfa(automata)
                        print("Transformed automata successfully")
                    elif command == "visualize":
                        visualize(automata)
                    elif command == "check":
                        if check_args(arguments):
                            if check(automata, *arguments):
                                print("Word is correct")
                            else:
                                print("Word is incorrect")

                    else:
                        if check_args(arguments):
                            try:
                                write(automata, *arguments)
                                print("Wrote successfully")
                            except FileNotFoundError:
                                print("Can't open output file!")

        except Exception as e:
            print(f"Unexpected error: {e}")

    else:
        if (len(args) < 1) or (args[1] != "="):
            print(f"Unknown expression: {' '.join(args)}")
        else:
            automata_name = args[0]
            pipeline = args[2:]
            if apply_operations(dict_automata, automata_name, pipeline):
                print(f"Successfully calculated and stored automata '{automata_name}'")


def run_nfa():
    """
    Реализуем REPL. Читаем из командной строки и вызываем соответствующую функцию.
    """
    dict_automata = {}
    while True:
        command_args = input(">>> ").split()

        if command_args:
            if command_args == ["exit"]:
                break
            elif command_args == ["clear"]:
                dict_automata = {}
            elif command_args == ["display_names"]:
                print(f"Automata names:\n{list(dict_automata.keys())}")
            else:
                execute_command(dict_automata, *command_args)


if __name__ == "__main__":
    print("App is started. Welcome, sir/madame!")
    run_nfa()
    print("App is terminated. Good day, sir/madame!")
