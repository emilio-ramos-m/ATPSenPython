import pulp

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_GG", pulp.LpMinimize)

# Example data: cost matrix (could be obtained from the document or defined by the user)
# Assume a 4-node problem for illustration (the matrix should be n x n for n nodes)
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

# Variables: x[i][j] is 1 if the tour goes from i to j
x = pulp.LpVariable.dicts("x", A, cat=pulp.LpBinary)

# GG specific variables: g[i][j] is the flow on arc from i to j
g = pulp.LpVariable.dicts("g", ((i, j) for i in range(1, n) for j in range(1, n) if i != j), lowBound=0, cat=pulp.LpContinuous)

#Funcion objetivo: Minimizar la suma de los costos de los arcos elegidos
prob += pulp.lpSum(costs[i][j] * x[i, j] for i in V for j in V if i != j)

# Restrictiones
for i in V:
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1#, f"Only_one_incoming_arc_{i}"
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1#, f"Only_one_outgoing_arc_{i}"

# Restriccion esoecifica de GG: Flujo de salida del nodo 1 es 1
for i in range(1, n):
    prob += g[1, i] == 1#, f"Flow_out_node_{i}"
    prob += pulp.lpSum(g[i, j] for j in range(1, n) if i != j) - pulp.lpSum(g[j, i] for j in range(1, n) if i != j) == 0#, f"Flow_conservation_node_{i}"

# Restriccion de capacidad en los arcos
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            prob += g[i, j] <= (n - 1) * x[i, j]#, f"Capacity_constraint_arc_{i}_{j}"

# Resolver el problema
prob.solve()

# Imprimir la solución
print("Status:", pulp.LpStatus[prob.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(prob.objective))

# Print the status of the solution
#print("Status:", pulp.LpStatus[prob.status])

# Print the optimal tour
#tour = [(i, j) for i in V for j in V if i != j and pulp.value(x[i, j]) == 1]
#print("Optimal Tour:", tour)

# Total cost of the tour
#total_cost = sum(costs[i][j] for i, j in tour)
#print("Total Cost of the Tour:", total_cost)
