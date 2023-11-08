import pulp
from extraerMatriz import read_atsp_file

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_MTZ", pulp.LpMinimize)

costs = read_atsp_file("instancias/inst1_10.atsp")

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
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1

# Eliminación de subtours de MTZ
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            prob += u[i] - u[j] + (n * x[i, j]) <= n - 1

# Resolver el problema
prob.solve()

# Imprimir la solución
print("Status:", pulp.LpStatus[prob.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(prob.objective))