import pulp
import itertools

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_DFJ", pulp.LpMinimize)

costs = [
    [9999, 20, 30, 10],
    [20, 9999, 15, 25],
    [30, 15, 9999, 5],
    [10, 25, 5, 9999]
]

# Conjunto de nodos y aristas
n = len(costs)
V = range(n)
A = [(i, j) for i in V for j in V if i != j]

# Example: Number of nodes
#n = 4  # You will have your own number of nodes from your data

# Crear variables de decision
x = pulp.LpVariable.dicts("x", A, cat=pulp.LpBinary)

# Example: Cost matrix
#costs = [[9999 if i == j else 1 for j in V] for i in V]  # Example costs, replace with your data

#Funcion objetivo: Minimizar la suma de los costos de los arcos elegidos
prob += pulp.lpSum(x[i, j] * costs[i][j] for i in V for j in V if i != j)

# Restricciones: cada nodo tiene exactamente un arco entrante y uno saliente
for i in V:
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1  # Exactly one outgoing arc
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1  # Exactly one incoming arc

# Eliminación de subtours
for s in range(2, n):
    for subset in itertools.combinations(V, s):
        prob += pulp.lpSum(x[i, j] for i in subset for j in subset if i != j) <= len(subset) - 1

# Solve the problem
prob.solve()

# Output the results
#for i in V:
#    for j in V:
#       if pulp.value(x[i, j]) == 1:
#           print(f"Node {i} -> Node {j}")

print("Status:", pulp.LpStatus[prob.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(prob.objective))
