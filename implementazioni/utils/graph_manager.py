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

    def generate_from_file(self,file_path):
        try:
            with open(file_path, 'r') as f:
                first_line=f.readline().split()
                if not first_line:
                    raise ValueError("Il file è vuoto")
                n= int(first_line[0])
                m=int(first_line[1])
                self.G.clear()
                self.G.add_nodes_from(range(n))

                for line in f:
                    if line.strip():
                        parts = line.split()
                        u,v= int(parts[0]), int(parts[1])
                        self.G.add_edge(u,v)
                m_actual = self.G.number_of_edges()
                print(f"Successo: Caricati {n} nodi e {m_actual} archi")
        except FileNotFoundError:
            print(f"Errore: Il file {file_path} non esiste")
        except Exception as e:
            print(f"Errore durante il caricamento : {e}")

    def load_coordinates_from_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                count =0
                for line in f:
                    parts = line.split()
                    if len(parts) >= 3:
                        node_id = int(parts[0])
                        x = float(parts[1])
                        y= float (parts[2])
                        if node_id in self.G.nodes:
                            self.G.nodes[node_id]['pos'] = (x,y)
                            count+=1
                        else:
                            print(f"Warning: nodo {node_id} trovato nel file.co ma non presente nel grafo")
            print(f"Successo: Caricate coordinate per {count} nodi")
        except FileNotFoundError:
            print(f"Errore: Il file di coordinate {file_path} non esiste.")
        except Exception as e:
            print(f"Errore durante il caricamento coordinate: {e}")

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
            return avg_potential * factor
        elif mode == "diameter_based":
            # B = factor * costo dell'arco che copre il diametro attuale
            perc = nx.periphery(self.G)
            d_cost = self.get_euclidean_cost(perc[0], perc[-1])
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
    gm = GraphManager(False)
    gm.generate_from_file("../datasets/simple_path/grafo.txt")
    gm.load_coordinates_from_file("../datasets/simple_path/grafo.co")
    print(f"Budget average: {gm.get_research_budget(factor=2)}")
    print(f"Budget diameter_based: {gm.get_research_budget(mode="diameter_based",factor=2)}")
    

    gm.visualize(show_diameter=True)
    