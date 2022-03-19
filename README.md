# Finite automata (NFA/DFA) realization

The application starts by using command `PYTHONPATH='.' python3 src/main.py` from `nfa` directory.

## Functionality:

1. Read automata from file: `read path_to_file`

2. Write automata to file: `write path_to_file`

3. Visualization of current automata: `visualization`

4. Checking of the word: `check word_to_check`

5. Transformation of current NFA to DFA: `transform`

6. Minimize current DFA: `minimize`

7. Exiting from application: `exit`


## Example of work:

```
read ./src/examples/nfa1.txt
visualize
transform
minimize
write ./src/examples/nfa1_out.txt
exit
```



## Our awesome team:

* Vadim: reading/writeing/visualization/data validation/linking code

* Fedor: transformation from nfa to dfa

* Vlad: checking of the word

* Elisey: minimization of dfa

