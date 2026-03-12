import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from algorithms.greedy_2sweep import greedy_solver
from algorithms.greedy_cost_aware import greedy_cost_aware
from utils.graph_manager import GraphManager

def run_experiment():
    gm= GraphManager()
    #gm.generate_random_with_coords(20,0.3)
    gm.generate_from_file("datasets/simple_path/grafo.txt")
    gm.load_coordinates_from_file("datasets/simple_path/grafo.co")
    for i in range(1,5):
        G_temp= gm.G.copy()

        budget = gm.get_research_budget(mode = "diameter_based", factor = float(i))
        cost_fn = gm.get_euclidean_cost
        delta = 3 #Matching
        gm.visualize(show_diameter= True, budget=budget)

        M, D, time, residual_budget =greedy_cost_aware(gm.G, delta, budget, cost_fn)
        
        print(f"greedy_solver ha eseguito in {time} secondi")
        print(f"greedy solver ha aggiunto questi shortcut edges: {M}")
        print(f"il diametro finale raggiunto è D = {D}")
        print(f"Ho ancora disponibile un budget pari a {residual_budget} ")

        gm.G.add_edges_from(M)
        gm.visualize(title=f"{i} Risultato Post ", show_diameter=True, added_edges=M, budget= budget)

        gm.G= G_temp.copy()
        plt.show()
    #X= np.array(X_list)
    #Y= np.array(Y_list)
    #plt.scatter(X,Y)
    plt.show()



if __name__ == "__main__":
    run_experiment()