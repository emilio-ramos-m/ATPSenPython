import pulp
from extraerMatriz import read_atsp_file

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_GG", pulp.LpMinimize)

costs = read_atsp_file("instancias/inst1_10.atsp")

# Conjunto de nodos y aristas
n = len(costs)
V = range(n)
A = [(i, j) for i in V for j in V if i != j]

# Crear variables de decision
x = pulp.LpVariable.dicts("x", A, cat=pulp.LpBinary)

# Variables especificas GG 
g = pulp.LpVariable.dicts("g", ((i, j) for i in V for j in V if i != j), lowBound=0, cat=pulp.LpContinuous)


#Funcion objetivo: Minimizar la suma de los costos de los arcos elegidos
prob += pulp.lpSum(costs[i][j] * x[i, j] for i in V for j in V if i != j)

# Restrictiones
for i in V:
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1

# Restriccion especifica de GG
for i in V:
    if(i>=1):
        prob += pulp.lpSum(g[(i,j)] for j in V if i != j) - pulp.lpSum(g[(j,i)] for j in V if j>=1 and i != j) == 1

# Restriccion de capacidad en los arcos
for i in V:
    for j in V:
        if i != j:
            prob += g[i, j] <= (n - 1) * x[i, j]

# Resolver el problema
prob.solve()

# Imprimir la solución
print("Status:", pulp.LpStatus[prob.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(prob.objective))


