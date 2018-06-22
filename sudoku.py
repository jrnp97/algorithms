"""
Sud-oku Solver.
"""

# HARD
sud_oku = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 3, 6, 0, 0, 0, 0, 0],
           [0, 7, 0, 0, 9, 0, 2, 0, 0],
           [0, 5, 0, 0, 0, 7, 0, 0, 0],
           [0, 0, 0, 0, 4, 5, 7, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 3, 0],
           [0, 0, 1, 0, 0, 0, 0, 6, 8],
           [0, 0, 8, 5, 0, 0, 0, 1, 0],
           [0, 9, 0, 0, 0, 0, 4, 0, 0]
           ]


# EASY 1
# sud_oku = [[0, 9, 2, 0, 0, 4, 7, 0, 0],
#            [1, 5, 0, 0, 6, 0, 2, 0, 8],
#            [0, 0, 0, 0, 1, 2, 0, 4, 9],
#            [0, 0, 0, 0, 5, 8, 6, 0, 0],
#            [8, 4, 0, 0, 3, 0, 0, 5, 2],
#            [0, 0, 3, 2, 9, 0, 0, 0, 0],
#            [6, 1, 0, 8, 4, 0, 0, 0, 0],
#            [2, 0, 5, 0, 7, 0, 0, 6, 1],
#            [0, 0, 7, 6, 0, 0, 8, 9, 0],
#            ]

# EASY 2
# sud_oku = [[0, 0, 0, 0, 9, 6, 4, 0, 1],
#            [1, 0, 9, 0, 0, 2, 7, 3, 0],
#            [0, 3, 4, 7, 0, 5, 2, 6, 0],
#            [3, 0, 6, 4, 0, 0, 0, 1, 2],
#            [7, 0, 1, 2, 6, 0, 3, 4, 0],
#            [0, 2, 0, 5, 3, 0, 0, 7, 0],
#            [2, 4, 0, 0, 5, 8, 0, 0, 3],
#            [9, 0, 0, 0, 0, 3, 8, 2, 4],
#            [0, 8, 3, 9, 2, 0, 0, 0, 7],
#            ]

def show_sud_oku(sud):
    init = [0, 8]
    i = [val for val in range(init[0], init[1] + 1)]
    j = 0
    cnt = 1
    print("*" * 21)
    while j < 9:
        print(f"{sud[i[0]]} {sud[i[1]]} {sud[i[2]]} | "
              f"{sud[i[3]]} {sud[i[4]]} {sud[i[5]]} | "
              f"{sud[i[6]]} {sud[i[7]]} {sud[i[8]]}")
        if cnt == 3:
            print("-" * 21)
            cnt = 0
        j += 1
        init[0] += 9
        init[1] += 9
        i = [val for val in range(init[0], init[1] + 1)]
        cnt += 1
    print("*" * 21)


def is_valid(number, structure, box, place):
    element_line_horizontal = [structure[j] for j in range(box[0], box[1] + 1)]

    if number in element_line_horizontal:
        return False
    else:

        row_0_position = place % 9
        element_index_vertical = [0 for _ in range(9)]
        element_index_vertical[0] = row_0_position
        element_id = 1
        while element_id < 9:
            element_index_vertical[element_id] += element_index_vertical[element_id - 1] + 9
            element_id += 1

        element_line_vertical = [structure[pos] for pos in element_index_vertical]

        if number in element_line_vertical:
            return False
        else:
            boxes_row_0_range = [(0, 2),
                                 (3, 5),
                                 (6, 8)]
            box_id = -1
            for b_id, box in enumerate(boxes_row_0_range):
                if (element_index_vertical[0] >= box[0]) and (element_index_vertical[0] <= box[1]):
                    box_id = b_id
                    break

            column_groups = [element_index_vertical[0:3:1],
                             element_index_vertical[3:6:1],
                             element_index_vertical[6:9:1]
                             ]
            column_g_id = -1
            for g_id, group in enumerate(column_groups):
                if place in group:
                    column_g_id = g_id
                    break

            quadrant_column = column_groups[column_g_id].copy()

            if element_index_vertical[0] == boxes_row_0_range[box_id][1]:
                temp = [[value - 2, value - 1, value] for value in quadrant_column]

            elif element_index_vertical[0] == boxes_row_0_range[box_id][0]:
                temp = [[value, value + 1, value + 2] for value in quadrant_column]

            else:
                temp = [[value - 1, value, value + 1] for value in quadrant_column]

            element_index_quadrant = [value for row in temp for value in row]
            quadrant = [structure[pos] for pos in element_index_quadrant]

            if number in quadrant:
                return False

    return True


def get_valid_numbers(sud_line, row_range, position):
    numbers = list(range(1, 10))
    valid = []
    for num in numbers:
        if is_valid(number=num, structure=sud_line, box=row_range, place=position):
            valid.append(num)

    return valid


def reset_sud(sud_line):
    temp = sud_line.copy()
    for idx, element in enumerate(temp):
        if type(element) == list:
            temp[idx] = 0
    return temp


def is_sud_valid(sud_line):
    status = []

    for element in sud_line:
        if element == 0 or type(element) == list:
            status.append(False)
        elif element < 0:
            status.append(None)
        else:
            status.append(True)

    if (not all(status) and status.count(True) < 17) or status.count(None) >= 1:
        return False
    elif status.count(True) >= 17:
        return True


def basic_solver(sud_line):
    position = 0
    modifications = 0
    row_range = [0, 8]
    possibilities_size = []
    while position < 81:
        if sud_line[position] == 0:
            validates = get_valid_numbers(sud_line=sud_line, row_range=row_range, position=position)
            possibilities_size.append(len(validates))
            sud_line[position] = validates if len(validates) > 1 else validates[0]
        else:
            possibilities_size.append(1)

        position += 1
        modifications += 1
        if modifications == 9:
            row_range[0] += 9
            row_range[1] += 9
            modifications = 0

    return possibilities_size


def any_change(sud_true, sud_result):
    status = []
    for true, res in zip(sud_true, sud_result):
        if true - res == 0:
            status.append(True)
        else:
            status.append(False)

    return not all(status)


def expert_solver(sud_line):
    pass


if __name__ == "__main__":
    s_deserializer = [value for row in sud_oku for value in row]
    print("Sud-oku to solver")
    show_sud_oku(s_deserializer)
    print("Solution : ")
    if is_sud_valid(s_deserializer):
        while True:
            origin = s_deserializer.copy()
            lenght = basic_solver(s_deserializer)
            result = reset_sud(s_deserializer)

            if any_change(origin, result):
                s_deserializer = result.copy()
            else:
                print("ERROR!!, basic mode is broken to iput sud-oku")
                break

            if sum(lenght) == 81:
                break
        show_sud_oku(s_deserializer)
    else:
        print("The elements on sud-oku is incorrect")
