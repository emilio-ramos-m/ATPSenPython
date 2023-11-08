import pulp
from extraerMatriz import read_atsp_file

# Crear problema de minimización
prob = pulp.LpProblem("ATSP_MTZ", pulp.LpMinimize)

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