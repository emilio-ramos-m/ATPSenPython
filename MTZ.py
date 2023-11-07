import pulp

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_MTZ", pulp.LpMinimize)

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

# Variables: x[i][j] es 1 si el tour va de i a j
x = pulp.LpVariable.dicts("x", A, cat=pulp.LpBinary)

# MTZ variables especificas: u[i] es la posición del nodo i en el tour
u = pulp.LpVariable.dicts("u", (i for i in V), lowBound=0, cat=pulp.LpContinuous)

#Funcion objetivo: Minimizar la suma de los costos de los arcos elegidos
prob += pulp.lpSum(costs[i][j] * x[i, j] for i in V for j in V if i != j)

# Restrictiones
for i in V:
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1#, f"Only_one_incoming_arc_{i}"
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1#, f"Only_one_outgoing_arc_{i}"

# Eliminación de subtours de MTZ
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            prob += u[i] - u[j] + (n * x[i, j]) <= n - 1

# Additional constraint for u[0] since it's the first node in the MTZ formulation
#prob += u[0] == 0

# Resolver el problema
prob.solve()

# Imprimir la solución
print("Status:", pulp.LpStatus[prob.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(prob.objective))

# Imprimir la solución
#print("Status:", pulp.LpStatus[prob.status])

# Print the optimal tour
#tour = [(i, j) for i in V for j in V if i != j and pulp.value(x[i, j]) == 1]
#print("Optimal Tour:", tour)

# Total cost of the tour
#total_cost = sum(costs[i][j] for i, j in tour)
#print("Total Cost of the Tour:", total_cost)
