import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from algorithms.greedy_2sweep import greedy_solver
from utils.graph_manager import GraphManager

def run_experiment():
    gm= GraphManager()
    gm.generate_from_file("datasets/simple_path/grafo.txt")
    gm.load_coordinates_from_file("datasets/simple_path/grafo.co")
    cost_fn = gm.get_euclidean_cost
    budget = gm.get_research_budget(mode = "average")
    delta = 1 #Matching
    M, D, time =greedy_solver(gm.G, delta, budget, cost_fn)
    print(f"greedy_solver ha eseguito in {time} secondi")
    print(f"greedy solver ha aggiunto questi shortcut edges: {M}")
    print(f"il diametro finale raggiunto è D = {D}")
    gm.visualize(show_diameter= True)



if __name__ == "__main__":
    run_experiment()