from map import Map
import time
import random

CROSS_NUMBER = 9


def equal_zero(row):
    for i in range(len(row)):
        if row[i] != 0:
            return False
    return True

def delete_zero_rows(legal_rows):
    return [row for row in legal_rows if not equal_zero(row)]

def generate_legal_rows(size, row_counts, legal_rows):
    if not row_counts:  # 终止条件：当没有更多的行计数时
        legal_rows.append([CROSS_NUMBER] * size)  # 修改这里，确保空行也是size长度
        return

    fd_for_first_element = size - sum(row_counts[1:]) - len(row_counts[1:]) - row_counts[0] + 1
    for i in range(fd_for_first_element):
        left = [CROSS_NUMBER for _ in range(i)] + [1] * row_counts[0]
        # 生成剩余部分的合法行，并与当前行组合
        legal_right_rows = []
        generate_legal_rows(size - len(left) - 1, row_counts[1:], legal_right_rows)
        for right_row in legal_right_rows:
            legal_rows.append((left + [CROSS_NUMBER] + right_row)[:size])

def generate_legal_rows_with_given_row(size, row_counts, row):
    legal_rows = []
    generate_legal_rows(size, row_counts, legal_rows)
    legal_rows = delete_zero_rows(legal_rows)
    # given row里面既有1也有9，返回的legal rows里面所有的row要在given row里面为1的地方全是1，
    # 在given row里面为9的地方全是9
    remove_indices = []
    for legal_row in legal_rows:
        for i in range(size):
            if row[i] != 0 and row[i] != legal_row[i]:
                remove_indices.append(legal_rows.index(legal_row))
                break
    for index in remove_indices[::-1]:
        legal_rows.pop(index)
    return legal_rows

def check_row_fill(size, row_count, row):
    current_row_count = []
    count = 0
    for i in range(size):
        if row[i] == 1:
            count += 1
        elif count:
            current_row_count.append(count)
            count = 0
    if count:
        current_row_count.append(count)
    return current_row_count == row_count

def check_column_fill(size, column_count, column):
    current_column_count = []
    count = 0
    for i in range(size):
        if column[i] == 1:
            count += 1
        elif count:
            current_column_count.append(count)
            count = 0
    if count:
        current_column_count.append(count)
    return current_column_count == column_count

def check_map_fill(size, row_counts, column_counts, map):
    for i in range(len(map)):
        if not check_row_fill(size, row_counts[i], map[i]):
            return False
    for i in range(size):
        if not check_column_fill(size, column_counts[i], [row[i] for row in map]):
            return False
    return True

def check_fill_cells_in_row(size, row_counts, row_number, row):
    fill_cells = []
    legal_rows = generate_legal_rows_with_given_row(size, row_counts, row)
    # print("Legal rows for row", row_number, ":", legal_rows)
    if not legal_rows:
        return fill_cells
    for i in range(size):
        if row[i] == 0:
            if all(r[i] == 1 for r in legal_rows):
                fill_cells.append((row_number, i+1))
    return fill_cells

def check_fill_cells_in_column(size, column_counts, column_number, column):
    fill_cells = []
    legal_columns = generate_legal_rows_with_given_row(size, column_counts, column)
    if not legal_columns:
        return fill_cells
    for i in range(size):
        if column[i] == 0:
            if all(r[i] == 1 for r in legal_columns):
                fill_cells.append((i+1, column_number))
    return fill_cells

def check_fill_cells_for_rows(size, row_counts, map):
    fill_cells = []
    for i in range(len(map)):
        fill_cells += check_fill_cells_in_row(size, row_counts[i], i+1, map[i])
    return fill_cells

def check_fill_cells_for_columns(size, column_counts, map):
    fill_cells = []
    for i in range(size):
        column = [row[i] for row in map]
        fill_cells += check_fill_cells_in_column(size, column_counts[i], i+1, column)
    return fill_cells

def check_fill_cells_for_map(size, row_counts, column_counts, map):
    fill_cells = []
    fill_cells += check_fill_cells_for_rows(size, row_counts, map)
    fill_cells += check_fill_cells_for_columns(size, column_counts, map)
    # 去重
    fill_cells = list(set(fill_cells))
    return fill_cells

def add_cross(size, row_count, row):
    '''
    Add cross(-1) to the row
    '''
    if check_row_fill(size, row_count, row):
        for i in range(size):
            if row[i] == 0:
                row[i] = CROSS_NUMBER
        return row
    else:
        legal_rows = generate_legal_rows_with_given_row(size, row_count, row)
        for i in range(size):
            if all(r[i] != 1 for r in legal_rows):
                row[i] = CROSS_NUMBER
        return row

def add_cross_to_map(size, row_counts, column_counts, map):
    for i in range(len(map)):
        map[i] = add_cross(size, row_counts[i], map[i])
    for i in range(size):
        column = [row[i] for row in map]
        column = add_cross(size, column_counts[i], column)
        for j in range(size):
            map[j][i] = column[j]
    return map

def sweep_once(size, row_counts, column_counts, map):
    fill_cells = check_fill_cells_for_map(size, row_counts, column_counts, map)
    if not fill_cells:
        return False
    for row, column in fill_cells:
        map[row-1][column-1] = 1
    # print("map after sweep:")
    # sweep_map = Map(size)
    # sweep_map.map = map
    # print(sweep_map)
    # print()
    # print("remaining zero cells:", get_zero_cells(size, map))
    return True

def check_row_fill(size, row_count, row):
    current_row_count = []
    count = 0
    for i in range(size):
        if row[i] == 1:
            count += 1
        elif count:
            current_row_count.append(count)
            count = 0
    if count:
        current_row_count.append(count)
    return current_row_count == row_count

def check_column_fill(size, column_count, column):
    current_column_count = []
    count = 0
    for i in range(size):
        if column[i] == 1:
            count += 1
        elif count:
            current_column_count.append(count)
            count = 0
    if count:
        current_column_count.append(count)
    return current_column_count == column_count

def check_map_fill(size, row_counts, column_counts, map):
    for i in range(len(map)):
        if not check_row_fill(size, row_counts[i], map[i]):
            return False
    for i in range(size):
        if not check_column_fill(size, column_counts[i], [row[i] for row in map]):
            return False
    return True

def sweep(size, row_counts, column_counts, map):
    while True:
        add_cross_to_map(size, row_counts, column_counts, map)
        if not sweep_once(size, row_counts, column_counts, map):
            break
    return check_map_fill(size, row_counts, column_counts, map)
                
def combine_and_trial(size, legal_rows, row_counts, column_counts, map_grid, answers, max_time=10):
    if time.time() - start_time > max_time:
        return
    if all(len(row) <= 1 for row in legal_rows):
        map_copy = []
        for i in range(size):
            if len(legal_rows[i]) == 1:
                map_copy.append(legal_rows[i][0])
            else:
                map_copy.append([CROSS_NUMBER] * size)
        if sweep(size, row_counts, column_counts, map_copy):
            answers.append([row[:] for row in map_copy])
        return
    sorted_indices = sorted(range(len(legal_rows)), key=lambda x: len(legal_rows[x]))
    for i in sorted_indices:
        if len(legal_rows[i]) > 1:
            for legal_row in legal_rows[i]:
                map_copy = [row[:] for row in map_grid]
                map_copy[i] = legal_row
                legal_rows_copy = [row for row in legal_rows]
                legal_rows_copy[i] = [legal_row]
                if sweep(size, row_counts, column_counts, map_copy):
                    answers.append([row[:] for row in map_copy])
                else:
                    combine_and_trial(size, legal_rows_copy, row_counts, column_counts, map_copy, answers, max_time)
    # 去重
    unique_answers = set(tuple(map(str, row)) for row in answers)  # 将每个地图转换为字符串的元组，然后转换为集合去重
    answers[:] = [list(map(eval, map_tuple)) for map_tuple in unique_answers]  # 将去重后的集合转换回二维列表形式

def brute_force_solve(size, row_counts, column_counts, max_time=10):
    answers = []
    map_grid = [[0] * size for _ in range(size)]
    if sweep(size, row_counts, column_counts, map_grid):
        answers.append([row[:] for row in map_grid])
    else:
        legal_rows = []
        for i in range(size):
            legal_rows.append(generate_legal_rows_with_given_row(size, row_counts[i], map_grid[i]))
        combine_and_trial(size, legal_rows, row_counts, column_counts, map_grid, answers, max_time)
    return answers

def check_row_legal(size, row_counts, row):
    legal_rows = generate_legal_rows_with_given_row(size, row_counts, row)
    for legal_row in legal_rows:
        for i in range(size):
            if row[i] != 0:
                if row[i] != legal_row[i]:
                    break
        else:
            return True
    return False

def check_column_legal(size, column_counts, column):
    legal_columns = generate_legal_rows_with_given_row(size, column_counts, column)
    for legal_column in legal_columns:
        for i in range(size):
            if column[i] != 0:
                if column[i] != legal_column[i]:
                    break
        else:
            return True
    return False

def check_map_legal(size, row_counts, column_counts, map):
    for i in range(len(map)):
        if not check_row_legal(size, row_counts[i], map[i]):
            return False
    for i in range(size):
        if not check_column_legal(size, column_counts[i], [row[i] for row in map]):
            return False
    return True

def get_zero_cells(size, map):
    zero_cells = []
    for i in range(size):
        for j in range(size):
            if map[i][j] == 0:
                zero_cells.append((i, j))
    return zero_cells

def try_fill_all(size, row_counts, column_counts, map, answers):
    zero_cells = get_zero_cells(size, map)
    if not zero_cells:
        if sweep(size, row_counts, column_counts, map):
            answers.append([row[:] for row in map])
        return
    else:
        for zero_cell in zero_cells:
            # 尝试将zero_cell设置为1
            map_copy = [row[:] for row in map]
            map_copy[zero_cell[0]][zero_cell[1]] = 1
            if sweep(size, row_counts, column_counts, map_copy):
                answers.append([row[:] for row in map_copy])
            if check_map_legal(size, row_counts, column_counts, map_copy):
                try_fill_all(size, row_counts, column_counts, map_copy, answers)
            
def try_fill_solve(size, row_counts, column_counts, answers):
    map_grid = [[0] * size for _ in range(size)]
    if sweep(size, row_counts, column_counts, map_grid):
        answers.append([row[:] for row in map_grid])
    else:
        try_fill_all(size, row_counts, column_counts, map_grid, answers)
    for answer in answers:
        if get_zero_cells(size, answer):
            answers.remove(answer)
        # 去重
        unique_answers = set(tuple(map(str, row)) for row in answers)  # 将每个地图转换为字符串的元组，然后转换为集合去重
        answers[:] = [list(map(eval, map_tuple)) for map_tuple in unique_answers]  # 将去重后的集合转换回二维列表形式

def Monte_Carlo_trial(size, legal_rows, row_counts, column_counts, map_grid, answers, max_time=10):
    if all(len(row) <= 1 for row in legal_rows):
        map_copy = []
        for i in range(size):
            if len(legal_rows[i]) == 1:
                map_copy.append(legal_rows[i][0])
            else:
                map_copy.append([0] * size)
        if sweep(size, row_counts, column_counts, map_copy):
            answers.append([row[:] for row in map_copy])
        return
    while time.time() - start_time < max_time:
        if answers:
            return
        sorted_indices = sorted(range(len(legal_rows)), key=lambda x: len(legal_rows[x]))
        for i in sorted_indices:
            if len(legal_rows[i]) > 1:
                legal_row = legal_rows[i][random.randint(0, len(legal_rows[i])-1)]
                map_copy = [row[:] for row in map_grid]
                map_copy[i] = legal_row
                legal_rows_copy = [row for row in legal_rows]
                legal_rows_copy[i] = [legal_row]
                Monte_Carlo_trial(size, legal_rows_copy, row_counts, column_counts, map_copy, answers)
    # 去重
    unique_answers = set(tuple(map(str, row)) for row in answers)  # 将每个地图转换为字符串的元组，然后转换为集合去重
    answers[:] = [list(map(eval, map_tuple)) for map_tuple in unique_answers]  # 将去重后的集合转换回二维列表形式

def Monte_Carlo_solve(size, row_counts, column_counts, answers, max_time=10):
    map_grid = [[0] * size for _ in range(size)]
    # if time.time() - start_time > max_time:
    #     return
    if sweep(size, row_counts, column_counts, map_grid):
        answers.append([row[:] for row in map_grid])
    else:
        legal_rows = []
        for i in range(size):
            legal_rows.append(generate_legal_rows_with_given_row(size, row_counts[i], map_grid[i]))
        Monte_Carlo_trial(size, legal_rows, row_counts, column_counts, map_grid, answers, max_time)


start_time = time.time()
size = 10
test_map = Map(size)
print(test_map)
row_counts = test_map.get_row_count()
col_counts = test_map.get_col_count()

# answers = brute_force_solve(size, row_counts, col_counts, max_time=20)
answers = []
# Monte_Carlo_solve(size, row_counts, col_counts, answers, max_time=20)
try_fill_solve(size, row_counts, col_counts, answers)

for answer in answers:
    answer_map = Map(size)
    answer_map.map = answer
    print(answer_map)

end_time = time.time()
print("Time used:", end_time - start_time, "s")



# # test
# size = 4
# test_map = [[0, 0, 1, 0],
#             [0, 1, 0, 0],
#             [1, 0, 0, 0],
#             [0, 0, 0, 1]]
# row_counts = [[1,1],[1],[1],[1]]
# col_counts = [[1,1],[1],[1],[1]]

# add_cross_to_map(size, row_counts, col_counts, test_map)
# print(test_map)


