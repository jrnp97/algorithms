"""
Soluciónador de Sudoku's.
"""
from random import randint

a = [[8, 0, 0], [0, 0, 0], [0, 0, 0],
     [0, 0, 3], [6, 0, 0], [0, 0, 0],
     [0, 7, 0], [0, 9, 0], [2, 0, 0],
     [0, 5, 0], [0, 0, 7], [0, 0, 0],
     [0, 0, 0], [1, 0, 0], [0, 3, 0],
     [0, 0, 1], [0, 0, 0], [0, 6, 8],
     [0, 0, 8], [5, 0, 0], [0, 1, 0],
     [0, 9, 0], [0, 0, 0], [4, 0, 0]
     ]

sudoku = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 3, 6, 0, 0, 0, 0, 0],
          [0, 7, 0, 0, 9, 0, 2, 0, 0],
          [0, 5, 0, 0, 0, 7, 0, 0, 0],
          [0, 0, 0, 0, 4, 5, 7, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 3, 0],
          [0, 0, 1, 0, 0, 0, 0, 6, 8],
          [0, 0, 8, 5, 0, 0, 0, 1, 0],
          [0, 9, 0, 0, 0, 0, 4, 0, 0]
          ]


def is_valid(number, structure, box, place):
    print(f"Numero a examinar {number}, en el rango {box}, será puesto en {place}")
    cube_line = [structure[j] for j in range(box[0], box[1] + 1)]   # Linea horizontal del numero
    print("-"*10, "Linea horizontal")
    print(cube_line)

    if number in cube_line:
        return False  # Si ya existe horizontalmente se responde negativamente
    else:

        initial = place % 9  # Consiguiendo punto en fila 0 verticalmente
        # Inicializando ruta de indices de vector vertical
        steps = [0 for _ in range(9)]
        steps[0] = initial
        i = 1
        while i < 9:
            steps[i] += steps[i-1] + 9
            i += 1

        other_places = [structure[pos] for pos in steps]  # Creando arreglo de item verticalmente

        print("-" * 10, "Linea Vertical")
        print(other_places)
        print(f"Indices - {steps}")

        if number in other_places:
            return False  # Si ya existe verticalmente se responde negativamente
        else:
            quadrant = [(0, 2),
                        (3, 5),
                        (6, 8)]  # Estableciendo limites de los "box" en el sudoku
            quad_id = -1
            # Hallando en que box se encuentra el numero
            for id, boxed in enumerate(quadrant):
                if (steps[0] >= boxed[0]) and (steps[0] <= boxed[1]):
                    quad_id = id
                    break

            # Grupos de posibles columnas en el box
            c_groups = [steps[0:3:1],
                        steps[3:6:1],
                        steps[6:9:1]
                        ]
            num_pos = -1
            for idx, group in enumerate(c_groups):
                if place in group:
                    num_pos = idx
                    break
            quadrant_column = c_groups[num_pos].copy()   # Se extraen los indices de los elem.. en el box

            # Calculando indices en el "box"
            if steps[0] == quadrant[quad_id][1]:  # Esta en la pared derecha
                temp = [[value - 2, value - 1, value] for value in quadrant_column]

            elif steps[0] == quadrant[quad_id][0]:  # Esta en la pared izquierda
                temp = [[value, value + 1, value + 2] for value in quadrant_column]

            else:  # Esta en el centro
                temp = [[value - 1, value, value + 1] for value in quadrant_column]

            # Deserializando en vector la matriz de indices generada
            indexes = [value for row in temp for value in row]
            # Extrayendo valores en el box
            quadranted = [structure[pos] for pos in indexes]

            print("-" * 10, f"Box #{quad_id}")
            print(quadranted)
            print(f"Indices - {indexes}")

            if number in quadranted:
                return False  # Si el numero se encuentra en el "box" se responde negativamente

    return True  # Si nada de lo anterior se impide se retorna positivamente


def show_sudoku(sudo):
    init = [0, 8]
    i = [val for val in range(init[0], init[1] + 1)]
    j = 0
    cnt = 1
    print("*" * 21)
    while j < 9:
        print(f"{sudo[i[0]]} {sudo[i[1]]} {sudo[i[2]]} | "
              f"{sudo[i[3]]} {sudo[i[4]]} {sudo[i[5]]} | "
              f"{sudo[i[6]]} {sudo[i[7]]} {sudo[i[8]]}")
        if cnt == 3:
            print("-" * 21)
            cnt = 0
        j += 1
        init[0] += 9
        init[1] += 9
        i = [val for val in range(init[0], init[1] + 1)]
        cnt += 1
    print("*" * 21)


if __name__ == "__main__":

    s_deserializer = [value for row in sudoku for value in row]  # Deserializando sudoku en vector

    idx = 0  # Comenzando en el indice 1
    cont = 0  # Contador de cambios realizados
    cube = [0, 8]  # Primer linea horizontal a generar

    while idx < 81:  # ciclo que se ejecutará hasta completar los 84 numeros del sudoku

        print("="*30)
        print(f"Analizando posición {idx}")
        print("-" * 20)
        if s_deserializer[idx] == 0:  # si el valor a interactuar se encuentra vacio

            num = randint(1, 9)  # Se genera un numero aleatorio entre 1 y 9
            salir = is_valid(number=num, structure=s_deserializer, box=cube, place=idx)  # Se verifica la validez
            c = 0
            while not salir:  # Ciclo que se ejecuta hasta encontrar un numero valido
                num = randint(1, 9)  # Generando nuevo numero
                salir = is_valid(number=num, structure=s_deserializer, box=cube, place=idx)  # Validando
                c += 1
                if c == 20:
                    exit(1)

            s_deserializer[idx] = num  # Asignando numero valido al indice
        else:
            print("Ninguna Accion realizada")
        idx += 1  # Se cuenta el numero completado
        cont += 1  # se cuenta el "cambio"

        show_sudoku(s_deserializer)  # Se muestra el proceso de asignanción
        print(f"Valor contador {cont}")
        if cont == 9:  # Si el contador llega a 9 cambios realizados se cambia la linea horizontal a manejar
            cube[0] += 9
            cube[1] += 9
            cont = 0

    print(s_deserializer)  # Se muestra arreglo resultante.



