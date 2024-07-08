from map import Map
import time

def generate_legal_rows(size, row_counts, legal_rows):
    if not row_counts:  # 终止条件：当没有更多的行计数时
        legal_rows.append([0] * size)  # 修改这里，确保空行也是size长度
        return

    fd_for_first_element = size - sum(row_counts[1:]) - len(row_counts[1:]) - row_counts[0] + 1
    for i in range(fd_for_first_element):
        left = [0 for _ in range(i)] + [1] * row_counts[0]
        # 生成剩余部分的合法行，并与当前行组合
        legal_right_rows = []
        generate_legal_rows(size - len(left) - 1, row_counts[1:], legal_right_rows)
        for right_row in legal_right_rows:
            legal_rows.append((left + [0] + right_row)[:size])

def generate_legal_rows_with_given_row(size, row_counts, row):
    legal_rows = []
    generate_legal_rows(size, row_counts, legal_rows)
    legal_rows = delete_zero_rows(legal_rows)
    return [r for r in legal_rows if all(r[i] == 1 for i in range(size) if row[i] == 1)]

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

def sweep_once(size, row_counts, column_counts, map):
    fill_cells = check_fill_cells_for_map(size, row_counts, column_counts, map)
    if not fill_cells:
        return False
    for row, column in fill_cells:
        map[row-1][column-1] = 1
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
        if not sweep_once(size, row_counts, column_counts, map):
            break
    return check_map_fill(size, row_counts, column_counts, map)
                
def combine_and_trial(size, legal_rows, row_counts, column_counts, map_grid, answers):
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
    for i in range(len(legal_rows)):
        if len(legal_rows[i]) > 1:
            for legal_row in legal_rows[i]:
                map_copy = [row[:] for row in map_grid]
                map_copy[i] = legal_row
                legal_rows_copy = [row for row in legal_rows]
                legal_rows_copy[i] = [legal_row]
                combine_and_trial(size, legal_rows_copy, row_counts, column_counts, map_copy, answers)
    # 去重
    unique_answers = set(tuple(map(str, row)) for row in answers)  # 将每个地图转换为字符串的元组，然后转换为集合去重
    answers[:] = [list(map(eval, map_tuple)) for map_tuple in unique_answers]  # 将去重后的集合转换回二维列表形式

def solve(size, row_counts, column_counts):
    answers = []
    map_grid = [[0] * size for _ in range(size)]
    if sweep(size, row_counts, column_counts, map_grid):
        answers.append([row[:] for row in map_grid])
    else:
        legal_rows = []
        for i in range(size):
            legal_rows.append(generate_legal_rows_with_given_row(size, row_counts[i], map_grid[i]))
        combine_and_trial(size, legal_rows, row_counts, column_counts, map_grid, answers)
    return answers

def equal_zero(row):
    for i in range(len(row)):
        if row[i] != 0:
            return False
    return True

def delete_zero_rows(legal_rows):
    return [row for row in legal_rows if not equal_zero(row)]

start_time = time.time()
size = 7
test_map = Map(size)
print(test_map)
row_counts = test_map.get_row_count()
col_counts = test_map.get_col_count()
answers = solve(size, row_counts, col_counts)
for answer in answers:
    answer_map = Map(size)
    answer_map.map = answer
    print(answer_map)

end_time = time.time()
print("Time used:", end_time - start_time, "s")



