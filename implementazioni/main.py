import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from algorithms.basic_greedy import greedy_basic_solver
from algorithms.greedy_cost_aware import greedy_cost_aware
from algorithms.optimal_backtrack import solve_optimal_backtracking
from utils.graph_manager import GraphManager

def run_multiple_experiments_with_graph():
    gm= GraphManager()
    #gm.generate_random_with_coords(20,0.3)
    radius = gm.suggest_rgg_radius(30)
    gm.generate_rgg(7, radius)
    # gm.generate_from_file("datasets/simple_path/grafo.txt")
    # gm.load_coordinates_from_file("datasets/simple_path/grafo.co")
    #for i in range(1,5):
    G_temp= gm.G.copy()
    X_labels = []
    Y_labels = []
    for i in range (1,20):
        X_labels.append(i)
        budget = gm.get_research_budget(mode = "average", factor = float(i))
        cost_fn = gm.get_euclidean_cost
        delta = 1 #Matching

        M, D, time, residual_budget =greedy_cost_aware(gm.G, delta, budget, cost_fn, peripheral_tolerance=1)
        Y_labels.append(D)
        # print(f"greedy_solver ha eseguito in {time} secondi")
        # print(f"greedy solver ha aggiunto questi shortcut edges: {M}")
        # print(f"il diametro finale raggiunto è D = {D}")
        # print(f"Ho ancora disponibile un budget pari a {residual_budget} ")

        gm.G.add_edges_from(M)

        gm.G= G_temp.copy()
    X = np.array(X_labels)
    Y = np.array(Y_labels)
    plt.scatter(X,Y)
    plt.plot(X,Y)
    plt.xlabel("Budget")
    plt.ylabel("Diameter of G'")
    plt.xticks(range(int(min(X)), int(max(X))+1))
    plt.yticks(range(int(max(Y))+1))
    #plt.grid(True)
    plt.show()

def run_experiment():
    gm= GraphManager()
    #gm.generate_random_with_coords(20,0.3)
    radius = gm.suggest_rgg_radius(12)
    gm.generate_rgg(12, radius)
    # gm.generate_from_file("datasets/simple_path/grafo.txt")
    # gm.load_coordinates_from_file("datasets/simple_path/grafo.co")

    G_temp= gm.G.copy()
    budget = gm.get_research_budget(mode = "average", factor = 5)
    cost_fn = gm.get_euclidean_cost
    delta = 2 #Matching
    gm.visualize(show_diameter= True, budget=budget)
    #--------------Greedy -------------------------------------------------------------------------------#

    M, D, time, residual_budget =greedy_cost_aware(gm.G, delta, budget, cost_fn, peripheral_tolerance=1)
    print(f"greedy_solver ha eseguito in {time} secondi")
    print(f"greedy solver ha aggiunto questi shortcut edges: {M}")
    print(f"il diametro finale raggiunto è D = {D}")
    print(f"Ho ancora disponibile un budget pari a {residual_budget} ")

    #---------------------------------------------------------------------------------------------#

    #---------------Backtrack---------------------------------------------------------------------#

    # M, D, time = solve_optimal_backtracking(gm.G, delta, budget,cost_fn)
    # print(f"optimal backtrack ha eseguito in {time} secondi")
    # print(f"optimal_backtrack ha aggiunto questi shortcut edges: {M}")
    # print(f"il diametro finale raggiunto è D = {D}")

    #------------------------------------------------------------------------------------------#

    #-------------Basic Greedy---------------------------------------------------------------#

    # M, D, time, residual_budget = greedy_basic_solver(gm.G, delta, budget, cost_fn)
    # print(f"basic greedy ha eseguito in {time} secondi")
    # print(f"basic greedyha aggiunto questi shortcut edges: {M}")
    # print(f"il diametro finale raggiunto è D = {D}")
    # print(f"Ho ancora disponibile un budget pari a {residual_budget} ")

    #------------------------------------------------------------------------------------#
    gm.G.add_edges_from(M)
    gm.visualize(title=f"Risultato Post ", show_diameter=True, added_edges=M, budget= budget)
    print(f"archi aggiunti : {len(M)}")
    gm.G= G_temp.copy()
    plt.show()


if __name__ == "__main__":
    run_experiment()