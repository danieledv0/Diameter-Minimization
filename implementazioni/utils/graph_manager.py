import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

class GraphManager:
    def __init__(self, directed=False):
        self.directed = directed
        self.G = nx.DiGraph() if directed else nx.Graph()
    
    def generate_random_with_coords(self, n, p, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        self.G = nx.fast_gnp_random_graph(n, p, seed=seed, directed=self.directed)

        if not self.directed:
            while not nx.is_connected(self.G):
                components = list(nx.connected_components(self.G))
                u = random.choice(list(components[0]))
                v = random.choice(list(random.choice(components[1:])))
                self.G.add_edge(u, v)

        for node in self.G.nodes():
            self.G.nodes[node]['pos'] = (np.random.uniform(0, 100), np.random.uniform(0, 100))

    def draw_diameter(self, ax, pos):
        """
        Evidenzia il diametro del grafo.
        Ritorna il valore del diametro calcolato.
        """
        if self.directed or not nx.is_connected(self.G):
            print("Il diametro è calcolabile solo per grafi non orientati e connessi.")
            return 0

        # Calcolo del diametro (massima distanza tra coppie)
        d_value = nx.diameter(self.G)
        
        # Trova i nodi periferici (eccentricità = diametro)
        perc = nx.periphery(self.G)
        u = perc[0]
        diameter_edges = []
        
        for v in perc:
            if nx.shortest_path_length(self.G, u, v) == d_value:
                path = nx.shortest_path(self.G, u, v)
                diameter_edges = list(zip(path, path[1:]))
                break
        
        # Evidenzia gli archi in rosso
        if diameter_edges:
            nx.draw_networkx_edges(
                self.G, pos, edgelist=diameter_edges, 
                edge_color='red', width=3, label=f"Diametro (D={d_value})", ax=ax
            )
        return d_value

    def visualize(self, title="analisi grafo BMD-DC", show_diameter=False):
        """
        Visualizza il grafo. Se show_diameter è True, viene evidenziato il diametro
        """
        pos = nx.get_node_attributes(self.G, 'pos')
        fig, ax = plt.subplots(figsize=(10, 8))

        # Disegno base (nodi e archi grigi trasparenti)
        nx.draw_networkx_edges(self.G, pos, edge_color='gray', alpha=0.3, ax=ax)
        nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=300, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=10, ax=ax)

        d_text = ""
        if show_diameter:
            d_val = self.draw_diameter(ax, pos)
            d_text = f"\nDiametro orginale: {d_val}"
            ax.legend()

        ax.set_title(title + d_text, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    gm = GraphManager(directed=False)
    gm.generate_random_with_coords(10, 0.3)
    gm.visualize(show_diameter=True)