import networkx as nx
import time
import numpy as np
import random

# Strategia:
#     Ad ogni iterazione si sceglie l'arco (u,v) non presente in G che massimizza
#     il rapporto: efficiency(u,v) = gain(u,v) / cost(u,v)
#     dove gain(u,v) = D_corrente - D_dopo_aggiunta(u,v).

def compute_diameter (G:nx.Graph):
    return nx.diameter(G)

def simulate_diameter_after_edge(G:nx.Graph, u: int, v:int):
    G.add_edge(u,v)
    d = nx.diameter(G)
    G.remove_edge(u,v)
    return d

def get_peripheral_nodes(G:nx.Graph, tolerance= 1):
    """Ritorna i nodi periferici o quasi del grafo corrente."
    Calcola l'eccentricità di ogni nodo con una BFS per nodo (O(nm))"
    poi seleziona quelli con ecc >= D - tolerance
    """
    ecc = nx.eccentricity(G) 
    D = max(ecc.values())
    D = max (ecc.values())
    res = []
    for v,e in ecc.items():
        if e>= D-tolerance:
            res.append(v)
    return res


def greedy_cost_aware(G: nx.Graph, delta, B, cost_func, peripheral_tolerance = 1):
    
    G_work = G.copy()
    n = G_work.number_of_nodes()
    added_degree = np.zeros(n, dtype = "uint32")
    M_added = []
    current_budget = B
    D_current = compute_diameter(G_work)

    start_time = time.time()

    while True:
        peri= get_peripheral_nodes(G_work, tolerance = 1) #nodi periferici o quasi
        feasible_peri= [] #nodi periferici a cui si può aggiungere ancora un arco
        for i in range(len(peri)):
            u = peri[i]
            if added_degree[u] < delta:
                feasible_peri.append(u)
        if len(feasible_peri) < 2: #se trovo meno di due nodi periferici , considero anche altri
            for u in G_work.nodes():
                if added_degree[u] < delta :
                    feasible_peri.append(u)

        if len(feasible_peri) <2:
            print("fine algoritmo, non ho più di due nodi fattibili")
            break

    
        candidate_couples = []
        for i in range (len(feasible_peri)):
            for j in range (i+1, len(feasible_peri)):
                u = feasible_peri[i]
                v = feasible_peri[j]
                if G_work.has_edge(u,v):
                    continue
                cost = cost_func (u,v)
                if cost > current_budget:
                    continue
                candidate_couples.append((u,v,cost))
        if candidate_couples == []:
            print("Nessuna coppia  candidata nel budget disponibile ")
            break

        best_edge = None
        best_efficiency= -np.inf
        best_gain = 0
        best_cost_val = np.inf
        best_new_D = D_current

        for u,v,cost in candidate_couples:
            new_D = simulate_diameter_after_edge(G_work, u, v)
            gain = D_current - new_D  #calcolo quanto ci guadagnerei
            if gain <=0:
                continue
            efficiency = gain/cost
            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_edge = (u,v)
                best_gain = gain
                best_cost_val = cost
                best_new_D = new_D
        
        if best_edge is None:
            print("Nessun arco riduce il diametro")
            break
        
        u, v = best_edge
        G_work.add_edge(u,v)
        M_added.append((u,v))
        added_degree[u] += 1
        added_degree[v] += 1
        current_budget -= best_cost_val
        D_current = best_new_D

        if D_current < 2:
            print("Diametro minimo raggiunto. stoppamo")
            break
    elapsed = time.time() - start_time
    return M_added, D_current, elapsed, current_budget



