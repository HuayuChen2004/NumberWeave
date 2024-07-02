import random

class Map:
    def __init__(self, size: int):
        self.size = size
        self.map = [[0 for _ in range(size)] for _ in range(size)]
        self.generate_map()

    def generate_map(self):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j] = random.randint(0, 1)

    def __str__(self):
        s = ""
        for i in range(self.size):
            for j in range(self.size):
                s += str(self.map[i][j]) + " "
            s += "\n"
        return s
    
    def get_row_count(self):
        row_count = []
        for i in range(self.size):
            row = self.map[i]
            one_row_count = []
            count = 0
            for j in range(self.size):
                if row[j] == 1:
                    count += 1
                elif count > 0:
                    one_row_count.append(count)
                    count = 0
            if count > 0:
                one_row_count.append(count)
            row_count.append(one_row_count)
        return row_count
    
    def get_col_count(self):
        col_count = []
        for i in range(self.size):
            col = [self.map[j][i] for j in range(self.size)]
            one_col_count = []
            count = 0
            for j in range(self.size):
                if col[j] == 1:
                    count += 1
                elif count > 0:
                    one_col_count.append(count)
                    count = 0
            if count > 0:
                one_col_count.append(count)
            col_count.append(one_col_count)
        return col_count

if __name__ == "__main__":
    m = Map(10)
    print(m)
    print(m.get_row_count())
    print(m.get_col_count())