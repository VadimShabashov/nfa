# Finite automata (NFA/DFA) realization

The application starts by using command `PYTHONPATH='.' python3 src/main.py` from `nfa` directory.

## Functionality:

1. Read all automata from file: `read path_to_file`

2. Write all automata to file: `write path_to_file`

3. Visualization of current automata: `visualization automata_name`

4. Checking of the word: `check automata_name word_to_check`

5. Automata transformation from NFA to DFA: `transform automata_name`

6. Minimize automata (valid only for DFA): `minimize automata_name`

7. Clear all automata from memory: `clear`

8. Show names of stored automata: `display_names`

9. Exiting from application: `exit`


## Example of work:

```
read ./src/examples/test1.json
display_names
visualize name
transform name
minimize name
a3 = name union name2
write a3 ./src/examples/out.json
exit
```



## Our awesome team:

* Vadim: reading/writing/visualization/data validation/linking code/CLI

* Fedor: transformation from nfa to dfa/data validation

* Vlad: checking of the word/diff/union/intersect

* Elisey: minimization of dfa/Kleene star/concat


## Things to improve:

1. Continue calculation wihout closing visualization (possible solution requires multithreading)

2. Allow `a1 = transform a2`

3. Make written files the same form as files for reading.

4. Allow long chains of operations `a = a1 union a2 concat (star a3)`

