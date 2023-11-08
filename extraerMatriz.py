def read_atsp_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Buscar dimensión de matriz
    dimension_line = next(line for line in lines if line.startswith('DIMENSION'))
    dimension = int(dimension_line.split(':')[1].strip())

    # Encontrar comienzo de matriz
    matrix_section_start = lines.index("EDGE_WEIGHT_SECTION\n") + 1
    matrix_section_end = matrix_section_start + dimension

    # Extraer la matriz
    matrix = []
    for line in lines[matrix_section_start:matrix_section_end]:
        row = list(map(int, line.split()))
        matrix.append(row)

    return matrix

def extraerMatrices():
    matrices = []
    matrix1 = read_atsp_file("instancias/inst1_10.atsp")
    matrix2 = read_atsp_file("instancias/inst2_10.atsp")
    matrix3 = read_atsp_file("instancias/inst3_10.atsp")
    matrix4 = read_atsp_file("instancias/inst4_10.atsp")
    matrix5 = read_atsp_file("instancias/inst5_12.atsp")
    matrix6 = read_atsp_file("instancias/inst6_12.atsp")
    matrix7 = read_atsp_file("instancias/inst7_12.atsp")
    matrix8 = read_atsp_file("instancias/inst8_15.atsp")
    matrix9 = read_atsp_file("instancias/inst9_15.atsp")
    matrix10 = read_atsp_file("instancias/inst10_15.atsp")
    matrices.append(matrix1)
    matrices.append(matrix2)
    matrices.append(matrix3)
    matrices.append(matrix4)
    matrices.append(matrix5)
    matrices.append(matrix6)
    matrices.append(matrix7)
    matrices.append(matrix8)
    matrices.append(matrix9)
    matrices.append(matrix10)
    return matrices


def print_matrix(matrix):
    for i in matrix:
        for j in i:
            print(j, end=' ')
        print("\n")

