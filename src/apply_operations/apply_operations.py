from src.automata import Automata
from src.transform.transform import intersect_or_union, diff, star, concat


def apply_operations(dict_automata, automata_name, pipeline):
    if not pipeline:
        print(f"Got an empty pipeline for {automata_name}")
        return False
    elif len(pipeline) == 1:
        # Случай переприсваивания автомата a = b
        if isinstance(pipeline[0], dict):
            dict_automata[automata_name] = Automata(pipeline[0])
        elif pipeline[0] in dict_automata:
            dict_automata[automata_name] = dict_automata[pipeline[0]]
        else:
            print(f"Unknown automata '{pipeline[0]}")
            return False

    elif len(pipeline) == 2:
        # Случай звезды Клини
        if pipeline[0] != "star":
            print(f"Expression has length 2, but it is not a Kleene star")
            return False
        else:
            if isinstance(pipeline[1], dict):
                dict_automata[automata_name] = star(Automata(pipeline[1]))
            elif pipeline[1] in dict_automata:
                dict_automata[automata_name] = star(dict_automata[pipeline[1]])
            else:
                print(f"Unknown automata '{pipeline[1]}")
                return False

    elif len(pipeline) == 3:
        # Случай остальных операций
        if isinstance(pipeline[0], dict):
            pipe_automata1 = Automata(pipeline[0])
        elif pipeline[0] in dict_automata:
            pipe_automata1 = dict_automata[pipeline[0]]
        else:
            print(f"Unknown automata '{pipeline[0]}")
            return False

        if isinstance(pipeline[2], dict):
            pipe_automata2 = Automata(pipeline[2])
        elif pipeline[2] in dict_automata:
            pipe_automata2 = dict_automata[pipeline[2]]
        else:
            print(f"Unknown automata '{pipeline[2]}")
            return False

        operation = pipeline[1]

        if operation == "diff":
            automata = diff(pipe_automata1, pipe_automata2)
            dict_automata[automata_name] = automata
        elif operation == "union":
            automata = intersect_or_union(pipe_automata1, pipe_automata2, True)
            # print(":Here")
            dict_automata[automata_name] = automata
        elif operation == "intersect":
            automata = intersect_or_union(pipe_automata1, pipe_automata2)
        elif operation == "concat":
            automata = concat(pipe_automata1, pipe_automata2)
        else:
            print(f"Unknown operation '{operation}'")
            return False

        dict_automata[automata_name] = automata
        return True

    else:
        print(f"Given expression is too long (allowed number of operations is 1)")
        return False
