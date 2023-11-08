import pulp
from itertools import combinations
from extraerMatriz import read_atsp_file

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_DFJ", pulp.LpMinimize)

costs = read_atsp_file("instancias/inst1_10.atsp")

costs=[[9999, 3, 5, 48, 48, 8, 8, 5, 5,3, 3, 0, 3, 5, 8, 8, 5],
   [3, 9999, 3, 48, 48, 8, 8, 5, 5, 0 ,0 ,3 ,0 ,3 ,8 ,8, 5],
   [5, 3, 9999, 72, 72, 48, 48, 24, 24, 3, 3, 5, 3, 0, 48, 48, 24],
   [48, 48, 74, 9999, 0, 6, 6, 12, 12, 48, 48, 48, 48, 74, 6, 6, 12],
   [48, 48, 74, 0, 9999, 6, 6, 12, 12, 48, 48, 48, 48, 74, 6, 6, 12],
   [8, 8, 50, 6, 6, 9999, 0, 8, 8, 8, 8, 8, 8, 50, 0, 0, 8],
   [8, 8, 50, 6, 6, 0, 9999, 8, 8, 8, 8, 8, 8,50, 0, 0, 8],
   [5, 5, 26, 12, 12, 8, 8, 9999, 0, 5, 5, 5, 5, 26, 8, 8, 0],
   [5, 5, 26, 12, 12, 8, 8, 0, 9999, 5, 5, 5, 5, 26, 8, 8, 0],
   [3, 0, 3, 48, 48, 8, 8, 5, 5, 9999, 0, 3, 0, 3, 8, 8, 5],
   [3, 0, 3, 48, 48, 8, 8, 5, 5, 0, 9999, 3, 0, 3, 8, 8, 5],
   [0, 3, 5, 48, 48, 8, 8, 5, 5, 3, 3, 9999, 3, 5, 8, 8, 5],
   [3, 0, 3, 48, 48, 8, 8, 5, 5, 0, 0, 3, 9999, 3, 8, 8, 5],
   [5, 3, 0, 72, 72, 48, 48, 24, 24, 3, 3, 5, 3, 9999, 48, 48, 24],
   [8, 8, 50, 6, 6, 0, 0, 8, 8, 8, 8, 8, 8, 50, 9999, 0, 8],
   [8, 8, 50, 6, 6, 0, 0, 8, 8, 8, 8, 8, 8, 50, 0, 9999, 8],
   [5, 5, 26, 12, 12, 8, 8, 0, 0, 5, 5, 5, 5, 26, 8, 8, 9999]]

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
