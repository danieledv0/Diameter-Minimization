import networkx as nx
import time
import random
import numpy as np

def solve_greedy_2sweep(G : nx.Graph, delta, B, cost_func):
    """
    Euristica 2sweep per un algoritmo veloce anche su dataset molto grandi
    """
    G_temp = G.copy()
    n = G_temp.number_of_nodes()
    M_added = []
    current_budget = B
    added_degree = np.zeros(n, dtype = "uint32")

    start_time = time.time()

    while current_budget > 0:
        valid_nodes = []
        for v in G_temp.nodes():
            if added_degree[v] < delta:
                valid_nodes.append(v)
        if not valid_nodes:
            break

        #tra i nodi validi, ne scelgo uno random u
        u = random.choice(valid_nodes)

        #Trovo un nodo valido v che massimizza d(u,v) 
        lengths = nx.single_source_shortest_path_length(G_temp, u)
        candidate_v = {}
        for v, dist in lengths.items():
            if v != u and added_degree[v]<delta:
                candidate_v[v]=dist
        v = max(candidate_v, key = candidate_v.get) #Prendo il v la cui distanza è massima
        cost = cost_func(u,v)
        if current_budget >= cost and not G_temp.has_edge(u,v):
            G_temp.add_edge(u,v)
            M_added.append((u,v))
            current_budget-= cost
            added_degree[u] += 1
            added_degree[v] += 1
        else:
            break
    elapsed = time.time() - start_time

    final_diameter = nx.diameter(G_temp)
    return M_added, final_diameter, elapsed, current_budget




    


