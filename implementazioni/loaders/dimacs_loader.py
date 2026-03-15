import networkx as nx

def load_dimacs_graph(file_path, directed = False):
    """
    Carica i grafi in formato DIMACS come grafi non diretti
    Ignora i pesi degli archi
    """
    G= nx.DiGraph() if directed else nx.Graph()
    with open (file_path, "r") as f:
        for line in f:
            if line.startswith('c') or not line.strip():
                continue

            parts = line.split()
            if parts[0] == "p":
                n_nodes = int(parts[2])
                G.add_nodes_from(range(n_nodes))
            
            elif parts[0] == "a":
                u = int(parts[1])-1 #Così gli ID dei nodi partono da zero
                v = int(parts[2])-1
                G.add_edge(u,v)
    return G

def load_dimacs_coords(G, file_path):
    """
    Carica le coordinate normalizzandole su uno spazio limitato
    """
    count = 0
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith('v'):
                parts = line.split()
                node_id = int(parts[1])-1
                longitude = float(parts[2])/ 1_000_000
                latitude = float(parts[3]) / 1_000_000
                if node_id in G:
                    G.nodes[node_id]["pos"] = (longitude, latitude)  #occhio che sono gradi di longitudine e latitudine
                    count += 1

    return count
    