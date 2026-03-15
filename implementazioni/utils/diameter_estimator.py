import networkx as nx
import random
#funzione da usare quando lavoro con dataset molto grandi,
#in cui il metodo nx.diameter() dura troppo
def get_diameter_estimate(G: nx.Graph, k=4): #Dopo 4 sweeps ho visto che converge
    """
    Stima il diametro usando k-sweeps. 
    Più k è alto, più la stima è precisa (si avvicina al diametro reale dal basso).
    Retsituisce diametro e i due nodi vertici del diametro individuato
    """
    if not nx.is_connected(G):
        #In caso il grafo non sia connesso, lavorerò solo sulla componente + grande
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()

    nodes = list(G.nodes())
    curr_node = random.choice(nodes)
    best_estimate = 0
    start_node = curr_node
    final_node = curr_node
    
    for i in range(k):
        lengths = nx.single_source_shortest_path_length(G, curr_node)
        farthest_node = max(lengths, key = lengths.get)
        dist = lengths[farthest_node]

        if dist > best_estimate :
            best_estimate = dist
            start_node = curr_node
            final_node = farthest_node
        
        if curr_node == farthest_node:
            curr_node = random.choice(nodes) #Per evitare loop infiniti
        else:
            curr_node = farthest_node # al prossimo ciclo lo sweep parte da qua
 
    return best_estimate , start_node , final_node