import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from algorithms.basic_greedy import greedy_basic_solver
from algorithms.greedy_cost_aware import greedy_cost_aware
from algorithms.optimal_backtrack import solve_optimal_backtracking
from algorithms.greedy_2sweep import solve_greedy_2sweep
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
    #gm.create_rgg(12)
    gm.generate_simple_from_file("datasets/simple_path/grafo.txt", "datasets/simple_path/grafo.co")

    G_temp= gm.G.copy()
    budget = gm.get_research_budget(mode = "diameter_based", factor = 3)
    cost_fn = gm.get_euclidean_cost
    delta = 1 #Matching
    gm.visualize(title = f"Situa iniziale",show_diameter= True, budget=budget)

    #--------------Greedy cost aware-------------------------------------------------------------------------------#

    M, D, time, residual_budget =greedy_cost_aware(gm.G, delta, budget, cost_fn, peripheral_tolerance=1)
    print(f"greedy_solver ha eseguito in {time} secondi")
    print(f"greedy solver ha aggiunto questi shortcut edges: {M}")
    print(f"il diametro finale raggiunto è D = {D}")
    print(f"Ho ancora disponibile un budget pari a {residual_budget} ")
    gm.G.add_edges_from(M)
    gm.visualize(title=f"exec_time: {time:.5f} Post greedy cost aware ", show_diameter=True, added_edges=M, budget= budget)
    print(f"archi aggiunti : {len(M)}")
    gm.G= G_temp.copy()

    #---------------------------------------------------------------------------------------------#

    #---------------Backtrack---------------------------------------------------------------------#

    # M, D, time = solve_optimal_backtracking(gm.G, delta, budget,cost_fn)
    # print(f"optimal backtrack ha eseguito in {time} secondi")
    # print(f"optimal_backtrack ha aggiunto questi shortcut edges: {M}")
    # print(f"il diametro finale raggiunto è D = {D}")
    # gm.G.add_edges_from(M)
    # gm.visualize(title=f"Risultato Post ", show_diameter=True, added_edges=M, budget= budget)
    # print(f"archi aggiunti : {len(M)}")
    # gm.G= G_temp.copy()

    #------------------------------------------------------------------------------------------#

    #-------------Basic Greedy---------------------------------------------------------------#

    M, D, time, residual_budget = greedy_basic_solver(gm.G, delta, budget, cost_fn)
    print(f"basic greedy ha eseguito in {time} secondi")
    print(f"basic greedyha aggiunto questi shortcut edges: {M}")
    print(f"il diametro finale raggiunto è D = {D}")
    print(f"Ho ancora disponibile un budget pari a {residual_budget} ")
    gm.G.add_edges_from(M)
    gm.visualize(title=f"exec_time: {time:.5f} Post basic greedy", show_diameter=True, added_edges=M, budget= budget)
    print(f"archi aggiunti : {len(M)}")
    gm.G= G_temp.copy()

    #------------------------------------------------------------------------------------#
    #------------Greedy 2 sweep------------------------------------------------------------#

    M,D,time, residual_budget = solve_greedy_2sweep(gm.G, delta, budget, cost_fn)
    print(f"greedy_2sweepha eseguito in {time} secondi")
    print(f"greedy_2swwep  ha aggiunto questi shortcut edges: {M}")
    print(f"il diametro finale raggiunto è D = {D}")
    print(f"Ho ancora disponibile un budget pari a {residual_budget} ")
    gm.G.add_edges_from(M)
    gm.visualize(title=f"exec_time: {time:.5f} Post greedy 2 sweep", show_diameter=True, added_edges=M, budget= budget)
    print(f"archi aggiunti : {len(M)}")
    gm.G= G_temp.copy()
    plt.show()

    #-----------------------------------------------------------------------------------------#

def run_big_experiment():
    gm= GraphManager(False)
    gm.generate_dimacs_graph("datasets/nyc_network/USA-road-d.NY.gr",
                             "datasets/nyc_network/USA-road-d.NY.co")
    budget = gm.get_research_budget(mode = "diameter_based", factor = 3)
    print(f"Baudget: {budget}")
    cost_fn = gm.get_euclidean_cost
    delta = 1 #Matching

if __name__ == "__main__":
    #run_experiment()
    run_big_experiment()