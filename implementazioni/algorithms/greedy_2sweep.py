import networkx as nx
import time
import numpy as np

def greedy_solver(G: nx.Graph, delta, B, cost_func):
    G_temp = G.copy()
    n= G_temp.number_of_nodes()
    M_added = [] #set di archi nuovi agiunti
    current_budget=B
    added_degree = np.zeros(n,dtype = "uint32") #memorizza i gradi aggiunti a ogni nodo
    D_val = nx.diameter(G_temp)
    start_time= time.time()
    while True:
        if not nx.is_connected(G_temp): break
        D_val = nx.diameter(G_temp) #diametro attuale
        found_edge_to_add= False
        perc = nx.periphery(G_temp) #inisieme di nodi la cui eccentricità è uguale al diametro del grafo
        for i in range(len(perc)):
            for j in range(i+1, len(perc)):
                u=perc[i]
                v=perc[j]
                cost = cost_func(u,v)
                add_condition= (not (G_temp.has_edge(u,v)) and
                        current_budget - cost >= 0 and
                        added_degree[u] < delta and
                        added_degree[v] < delta
                        )
                if add_condition:
                    G_temp.add_edge(u,v)
                    M_added.append((u,v))
                    added_degree[u]+=1
                    added_degree[v]+=1
                    current_budget -= cost
                    print(f"Aggiunto arco ({u} , {v}) - Costo: {cost:.2f}")
                    found_edge_to_add= True
                    break
            if found_edge_to_add: break #raggiunto il minimo possibile
        if not found_edge_to_add:
            break
        if D_val < 2:
            break
    elapse = time.time()-start_time
    return M_added , D_val, elapse,  current_budget

