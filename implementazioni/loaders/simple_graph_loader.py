import networkx as nx

def load_graph_from_file(file_path, directed=False):
    G = nx.DiGraph() if directed else nx.Graph()
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if not lines: return G
            
            header = lines[0].split()
            n = int(header[0])
            G.add_nodes_from(range(n))

            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    u, v = int(parts[0]), int(parts[1])
                    G.add_edge(u, v)
        return G
    except Exception as e:
        print(f"Errore caricamento grafo: {e}")
        return G

def apply_coordinates(G, file_path):
    count = 0
    try:
        with open(file_path, "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3:
                    node_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                    if node_id in G.nodes:
                        G.nodes[node_id]['pos'] = (x, y)
                        count += 1
        return count
    except Exception as e:
        print(f"Errore coordinate: {e}")
        return 0