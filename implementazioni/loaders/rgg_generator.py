import networkx as nx
import numpy as np
import random

def suggest_rgg_radius(n, bbox=(100.0, 100.0), factor=1.5):
    area = bbox[0] * bbox[1]
    r_critical = np.sqrt(np.log(n) * area / (np.pi * n))
    return round(factor * r_critical, 2)

def generate_rgg(n, radius, bbox=(100.0, 100.0), seed=42, ensure_connected=True):
    """ 
    Genera Random Geometric Graph : n nodi disposti
    uniformemente sul piano cartesiano, con archi tra coppie
    a distanza <= radius
    """
    rng = np.random.default_rng(seed)
    random.seed(seed)
    G = nx.Graph()

    xs = rng.uniform(0, bbox[0], n)
    ys = rng.uniform(0, bbox[1], n)
    pos_array = np.column_stack([xs, ys])

    for i in range(n):
        G.add_node(i, pos=(float(xs[i]), float(ys[i])))
    
    for i in range(n):
        diffs = pos_array[i+1:] - pos_array[i]
        dists = np.linalg.norm(diffs, axis=1)
        neighbors = np.where(dists <= radius)[0] + (i+1)
        for j in neighbors:
            G.add_edge(i, int(j))

    if ensure_connected:
        while not nx.is_connected(G):
            components = list(nx.connected_components(G))
            best_u, best_v, best_dist = None, None, np.inf
            for ci in range(len(components)):
                for cj in range(ci + 1, len(components)):
                    sample_i = random.sample(list(components[ci]), min(40, len(components[ci])))
                    sample_j = random.sample(list(components[cj]), min(40, len(components[cj])))
                    for u in sample_i:
                        for v in sample_j:
                            # Calcolo distanza euclidea al volo
                            pos_u = np.array(G.nodes[u]["pos"])
                            pos_v = np.array(G.nodes[v]["pos"])
                            d = np.linalg.norm(pos_u - pos_v)
                            if d < best_dist:
                                best_dist, best_u, best_v = d, u, v
            G.add_edge(best_u, best_v)

    G.graph.update({"type": "RGG", "radius": radius, "bbox": bbox})
    return G


def generate_random_with_coords(n, p, directed=False, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    G = nx.fast_gnp_random_graph(n, p, seed=seed, directed=directed)

    if not directed:
        while not nx.is_connected(G):
            components = list(nx.connected_components(G))
            u = random.choice(list(components[0]))
            v = random.choice(list(random.choice(components[1:])))
            G.add_edge(u, v)

    for node in G.nodes():
        G.nodes[node]['pos'] = (np.random.uniform(0, 100), np.random.uniform(0, 100))
    return G