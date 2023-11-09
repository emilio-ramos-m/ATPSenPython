import pulp
from itertools import combinations
from extraerMatriz import read_atsp_file

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_DFJ", pulp.LpMinimize)

# Se carga el archivo con la matriz de costos
costs = read_atsp_file("instancias/inst1_10.atsp")

# Conjunto de nodos y aristas
n = len(costs)
V = range(n)
A = [(i, j) for i in V for j in V if i != j]

# Crear variables de decision
x = pulp.LpVariable.dicts("x", A, cat=pulp.LpBinary)

#Funcion objetivo: Minimizar la suma de los costos de los arcos elegidos
prob += pulp.lpSum(x[i, j] * costs[i][j] for i in V for j in V if i != j)

# Restricciones
for i in V:
    prob += pulp.lpSum(x[i, j] for j in V if i != j) == 1 
    prob += pulp.lpSum(x[j, i] for j in V if i != j) == 1  

# Eliminación de subtours
for s in range(2, n):
    for subset in combinations(V, s):
        prob += pulp.lpSum(x[i, j] for i in subset for j in subset if i != j) <= len(subset) - 1

# Resolver el problema
prob.solve()

# Imprimir la solución
print("Status:", pulp.LpStatus[prob.status])
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Optimal value =", pulp.value(prob.objective))
