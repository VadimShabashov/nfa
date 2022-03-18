class Automata:
    def __init__(self, data):
        self.glossary = data["glossary"]
        self.states = data["states"]
        self.initial_state = data["initial_state"]
        self.terminal_states = data["terminal_states"]
        self.edges = data["edges"]
        self.edges_epsilon = data["edges_epsilon"]
        self.is_dfa = data["is_dfa"]
