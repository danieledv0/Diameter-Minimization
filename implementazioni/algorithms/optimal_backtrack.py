import networkx as nx
import time
import numpy as np
from itertools import combinations

def solve_optimal_backtracking(G: nx.Graph, delta, B, cost_func):
    """
    Risolve il BDM-DC ottimalmente, applicabile solo 
    a grafi di piccole dimensioni
    """
    start_time = time.time()
    #Identifico tutti i possibili archi candidati (E^c)
    nodes = list(G.nodes())
    candidates = []
    for u,v in combinations(nodes, 2):
        if not G.has_edge(u,v):
            candidates.append((u,v,cost_func(u,v)))
    best_diameter = nx.diameter(G)
    best_M= []
    
    def backtrack(idx, current_G, current_B, added_degree):
        nonlocal best_diameter, best_M
        try:
            current_d = nx.diameter(current_G)
            if current_d < best_diameter:
                best_diameter = current_d
                best_M = list(current_G.edges())
                original_edges = set(G.edges())
                best_M = [e for e in current_G.edges() if e not in original_edges and (e[1], e[0]) not in original_edges]
        except nx.NetworkXError: 
            pass
        
        if idx == len(candidates) or best_diameter <= 2:
            return

        
        u, v, cost = candidates[idx]

        
        if current_B >= cost and added_degree[u] < delta and added_degree[v] < delta:
            current_G.add_edge(u, v)
            added_degree[u] += 1
            added_degree[v] += 1
            
            backtrack(idx + 1, current_G, current_B - cost, added_degree)
            
            
            current_G.remove_edge(u, v)
            added_degree[u] -= 1
            added_degree[v] -= 1

        
        backtrack(idx + 1, current_G, current_B, added_degree)

    initial_added_degree = {node: 0 for node in G.nodes()}
    backtrack(0, G.copy(), B, initial_added_degree)
    
    execution_time = time.time() - start_time
    return best_M, best_diameter, execution_time