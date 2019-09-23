#! /usr/bin/python3

# Search Space:
# The search space for each movement would depend on two factors:
#   1. Which side the lamp is currently at.
#   2. Who is at the side where the lamp is at.

# Initial State:
# In the beginning we would have everyone on the left side and no one on the right side.
# Since we will represent the people present with a bit flip when on, they are present, the initial
# state would be (31, 0).

# Goal State:
# Since the goal state would be to have everyone on the right side of the bridge, the
# representation state would be (0, 31).

# Rules:
# - Only 2 people can be bit flipped at the same time where we take the max(cost1, cost2) as cost.
# - Cost can not exceed the hard limit of 30.
# - 

# Cost Function:

# Heuristic Function:

# Search Tree Generation:
# Output by matplotlib+networkx

from collections import defaultdict
import math
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

# Dijkstra map containing the minimum cost for different states.
visited = defaultdict(lambda:None)

# Fixed costs for the speed of individuals.
cost = [1, 3, 6, 8, 12]
# Log capturing list.
path_expl = []
# Hard-coded max limit.
max_cost = 30

# Graph for visualization.
G = nx.Graph()
all_edges = [] 
answer_edges = []

def min(a, b):
    return a if a<b else b

def max(a, b):
    return a if a>b else b

def cost_function():
    return 1

def heuristic_function():
    return 1

def bitflip(current_state, i, j=None):
    bitmask = (1<<i)|(1<<j) if j else (1<<i)
    new_left = current_state[0]^bitmask
    new_right = current_state[1]^bitmask
    return (new_left, new_right)

def handle_nx_graph():
    red_edges = []
    black_edges = []

    G.add_edges_from(all_edges)

    values = [0.25 for x in all_edges]

    pos = graphviz_layout(G, prog='dot')
    #pos = nx.spring_layout(G, k=5/math.sqrt(G.order()))
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                       node_size = 800)
    nx.draw_networkx_labels(G, pos)

    red_edges_set = set(answer_edges)
    for x in all_edges:
        if x in red_edges_set:
            red_edges.append(x)
        else:
            black_edges.append(x)

    nx.draw_networkx_edges(G, pos, edgelist=black_edges, edge_color='b', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)

def dijkstra(current_state, lamp_left, current_cost):
    if current_cost > max_cost:
        return False
    
    # Update visited with min()
    visited[current_state] = min(visited[current_state], current_cost) if visited[current_state] else current_cost 

    # Check for final state to finish recursion.
    if current_state == (0, 31):
        return True

    possible = []
    # Create a list of possible moves.
    if lamp_left:
        for i in range(len(cost)-1):
            if (current_state[0] & 1<<i):
                for j in range(i+1, len(cost)):
                    possible.append((i, j))
    else:
        for i in range(len(cost)):
            if (current_state[1] & 1<<i):
                possible.append((i, None))
    
    # Sort the possible combination based on cost+heuristic.
    possible.sort(key=lambda t: cost_function()+heuristic_function())

    # Recurse through the best costly and heuristical move.
    for i, j in possible:
        # Calculate new state.
        new_state = bitflip(current_state, i, j)
        all_edges.insert(0, (current_state, new_state))
        if dijkstra(new_state, not lamp_left, current_cost+max(cost[i], cost[j] if j else -1)):
            # Log what action was done.
            if lamp_left:
                path_expl.insert(0, 'Took %d %d to the right\t\tcurrent_cost: %d'%(cost[i], cost[j], current_cost+max(cost[i], cost[j])))
            else:
                path_expl.insert(0, 'Returned %d to the left\t\tcurrent_cost: %d'%(cost[i], current_cost+cost[i]))
            # Include correct edge as answer.
            answer_edges.insert(0, (current_state, new_state))
            return True
    
    return False

def main():
    # Initial state.
    initial_state = (31, 0)
    test_state = (0, 31)
    # Initial lamp position; True is when lamp is on the left.
    initial_lamp_position = True
    # Initial cost.
    initial_cost = 0

    # This function should return True if it found a solution. 
    dijkstra(initial_state, initial_lamp_position, initial_cost)
    
    # path_expl should be empty list if no solution was found.
    for text in path_expl:
        print(text)
    
    # Handle graph generator.
    handle_nx_graph()

    # Show graph using matplotplt.
    plt.show()

if __name__ == '__main__':
    main()