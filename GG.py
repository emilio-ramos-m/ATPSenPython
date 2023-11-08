import pulp
from extraerMatriz import read_atsp_file

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_GG", pulp.LpMinimize)

costs = read_atsp_file("instancias/inst1_10.atsp")

# Conjunto de nodos y aristas
n = len(costs)
V = range(n)
A = [(i, j) for i in V for j in V if i != j]

# Variables: x[i][j] is 1 if the tour goes from i to j
x = pulp.LpVariable.dicts("x", A, cat=pulp.LpBinary)

# GG specific variables: g[i][j] is the flow on arc from i to j
g = pulp.LpVariable.dicts("g", ((i, j) for i in V for j in V if i != j), lowBound=0, cat=pulp.LpContinuous)


#Funcion objetivo: Minimizar la suma de los costos de los arcos elegidos
prob += pulp.lpSum(costs[i][j] * x[i, j] for i in V for j in V if i != j)

# Restrictiones
for i in V:
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1#, f"Only_one_incoming_arc_{i}"
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1#, f"Only_one_outgoing_arc_{i}"

# Restriccion esoecifica de GG: Flujo de salida del nodo 1 es 1
for i in V:
    if(i>=1):
        prob += pulp.lpSum(g[(i,j)] for j in V if i != j) - pulp.lpSum(g[(j,i)] for j in V if j>=1 and i != j) == 1

# Restriccion de capacidad en los arcos
for i in V:
    for j in V:
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


