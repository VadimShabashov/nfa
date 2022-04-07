import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from src.visualization.edge_labels import modified_draw_networkx_edge_labels


def visualize(automata):
    graph = nx.MultiDiGraph()

    plt.figure(1, figsize=(12, 12))

    node_list = automata.states
    initial_state = automata.initial_state
    terminal_states = automata.terminal_states
    edges_list = automata.edges
    edges_epsilon_list = automata.edges_epsilon

    # Создаем словарь из ребра и его названия
    edge_names = {}
    for state, values in edges_list.items():
        for other_state, edge_name in values:
            if (state, other_state) in edge_names:
                edge_names[(state, other_state)] += "; " + edge_name
            else:
                edge_names[(state, other_state)] = edge_name
    # Добавляем epsilon ребра
    for state, values in edges_epsilon_list.items():
        for other_state in values:
            if (state, other_state) in edge_names:
                edge_names[(state, other_state)] += "; " + chr(949)
            else:
                edge_names[(state, other_state)] = chr(949)

    # Добавляем ребра и вершины
    graph.add_nodes_from(node_list)
    graph.add_edges_from(edge_names.keys())

    # Задаем layout для вершин
    pos = nx.planar_layout(graph)

    # Ищем начальное и терминальные состояния, чтобы пометить их цветом.
    # Цвета выбираются так:
    # Желтый - начальное состояние
    # Красный - терминальное состояние
    # Розовый - остальные состояния
    initial_state_pos = node_list.index(initial_state)
    terminal_states_pos = [ind for ind, state in enumerate(node_list) if state in terminal_states]
    node_color = ['cyan' if (ind == initial_state_pos) and (ind in terminal_states_pos) else
                  'yellow' if (ind == initial_state_pos) else
                  'orange' if ind in terminal_states_pos else
                  'magenta' for ind in range(len(node_list))]

    # Изгиб ребер
    rad = 0.2

    nx.draw_networkx(graph, pos=pos, nodelist=node_list, node_color=node_color,
                     connectionstyle=f'arc3, rad = {rad}')

    # Модифицированная функция добавления названий к искривленным дугам.
    modified_draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_names, rad=rad)

    # Легенда
    legend_elements = [Line2D([0], [0], marker='o', label='Начальное + терминальное',
                              markerfacecolor='cyan', markeredgecolor='black', markersize=13),
                       Line2D([0], [0], marker='o', label='Начальное состояние',
                              markerfacecolor='yellow', markeredgecolor='black', markersize=13),
                       Line2D([0], [0], marker='o', label='Терминальное состояние',
                              markerfacecolor='orange', markeredgecolor='black', markersize=13),
                       Line2D([0], [0], marker='o', label='Остальные состояния',
                              markerfacecolor='magenta', markeredgecolor='black', markersize=13)]
    plt.legend(handles=legend_elements)

    plt.show()
