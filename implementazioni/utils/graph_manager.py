import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from loaders.rgg_generator import generate_rgg, suggest_rgg_radius, generate_random_with_coords
from loaders.simple_graph_loader import load_graph_from_file, apply_coordinates
from loaders.dimacs_loader import load_dimacs_graph , load_dimacs_coords


class GraphManager:
    def __init__(self, directed=False):
        self.directed = directed
        self.G = nx.DiGraph() if directed else nx.Graph()
    
    def create_rgg(self, n):
        """ 
        Genera Random Geometric Graph : n nodi disposti
        uniformemente sul piano cartesiano, con archi tra coppie
        a distanza <= radius
        """
        radius = suggest_rgg_radius(n)
        self.G = generate_rgg(n , radius)
    
    def generate_simple_from_file(self, graph_path, coord_path):
        """
        Carica grafo semplice dai file .txt e .co
        """
        self.G = load_graph_from_file(graph_path)
        apply_coordinates(self.G, coord_path)

    def generate_dimacs_graph(self, graph_path, coord_path):
        self.G = load_dimacs_graph(graph_path)
        count = load_dimacs_coords(self.G, coord_path)
        print(f"Dataset caricato: {self.G.number_of_nodes()} nodi, "
              f"{self.G.number_of_edges()} archi. Coordinate per {count} nodi.")
        
    def get_euclidean_cost(self, u, v):
        coordinates_u = np.array(self.G.nodes[u]["pos"])
        coordinates_v =np.array(self.G.nodes[v]["pos"])
        return np.linalg.norm(coordinates_u - coordinates_v)

    def get_research_budget(self, mode="average", factor=5.0):
        """
        Ritorna un budget B calcolato secondo criteri di ricerca: "average" o "diameter_based"
        """
        nodes = list(self.G.nodes())
        potential_costs = []
        # Campionamento degli archi potenziali (E^c)
        # Se il grafo è grande, meglio campionare a caso per velocità
        sample_size = min(1000, len(nodes) * (len(nodes)-1) // 2)
        for _ in range(sample_size):
            u, v = random.sample(nodes, 2)
            if not self.G.has_edge(u, v):
                potential_costs.append(self.get_euclidean_cost(u, v))
                
        avg_potential = np.mean(potential_costs)
        
        if mode == "average":
            print(f"Unità di misura del budget in mode average: {avg_potential}")
            return avg_potential * factor
        elif mode == "diameter_based":
            # B = factor * costo dell'arco che copre il diametro attuale
            perc = nx.periphery(self.G)
            d_cost = self.get_euclidean_cost(perc[0], perc[-1])
            #print(f"Unità di misura del budget in mode diameter: {d_cost}")
            return d_cost * factor
    
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


    def visualize(self, title="analisi grafo BMD-DC", show_diameter=False, added_edges= None, budget = None):
        """
        Visualizza il grafo. Se show_diameter è True, viene evidenziato il diametro
        """
        pos = nx.get_node_attributes(self.G, 'pos')
        fig, ax = plt.subplots(figsize=(10, 8))
        # ottieni il window manager
        manager = plt.get_current_fig_manager()
        # imposta posizione e dimensione: width x height + x + y
        if not added_edges :
            manager.window.wm_geometry("+100+100")
        else:
            manager.window.wm_geometry("+1300+100")

        # Disegno base (nodi e archi grigi trasparenti)
        nx.draw_networkx_edges(self.G, pos, edge_color='gray', alpha=0.3, ax=ax)
        #Disegno archi aggiunti
        if added_edges:
            nx.draw_networkx_edges(
                self.G, pos, edgelist=added_edges, 
                edge_color='green', width=1, label="Shortcuts Aggiunti", ax=ax
            )
            edge_labels= {}
            for u, v in added_edges:
                costo = self.get_euclidean_cost(u,v)
                edge_labels[(u,v)] = f"{costo:.2f}"
            nx.draw_networkx_edge_labels(
                self.G, pos, 
                edge_labels=edge_labels, 
                font_color='green', 
                font_size=12,
                label_pos=0.5, # 0.5 è esattamente a metà dell'arco
                ax=ax
            )
        nx.draw_networkx_nodes(self.G, pos, node_color='lightblue', node_size=500, ax=ax)
        nx.draw_networkx_labels(self.G, pos, font_size=10, ax=ax)

        d_text = ""
        if show_diameter:
            d_val = self.draw_diameter(ax, pos)
            d_text = f"\nDiametro attuale: {d_val}"
            ax.legend()
        b_text= f"  Budget ({budget:.2f} )"

        ax.set_title(title + b_text + d_text, fontsize=14, fontweight='bold')
        plt.tight_layout()
        #plt.show()


if __name__ == "__main__":
    gm= GraphManager(False)
    gm.generate_dimacs_graph("datasets/nyc_network/USA-road-d.NY.gr",
                             "datasets/nyc_network/USA-road-d.NY.co")