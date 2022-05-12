'''
The grid below shows the current schedule for a certain group of teachers (16 different teachers) and the classrooms they are assigned for the school year. We want to minimize the number of different classrooms a teacher needs to be in (minimize or avoid a teacher having three classrooms) but also maximize the number of teachers who only have one classroom. So teachers are allowed to move up and down columns (change rooms), but are not allowed to move across (change their schedule).
'''

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import random


def teacher_num_rooms(data: np.ndarray) -> dict[int, int]:
    num_rooms = defaultdict(list)

    for i in range(len(data)):
        for j in range(len(data[i])):
            value = data[i][j]
            if value == 0:
                continue
            num_rooms[value].append(i)

    for key, value in num_rooms.items():
        num_rooms[key] = len(Counter(value))

    # num_rooms = dict(sorted(num_rooms.items()))

    return num_rooms


def calc_fitness_values(num_rooms):
    num_one_classroom_teachers = list(num_rooms.values()).count(1)

    error = 0
    for value in num_rooms.values():
        error += (value - 1)**2
    error /= len(num_rooms)

    return num_one_classroom_teachers, error


data_frame: pd.DataFrame = pd.read_excel('data.xlsx', index_col=0)

periods: np.ndarray = data_frame.index.values.astype(int)
classrooms: np.ndarray = data_frame.columns.values.astype(str)

data = data_frame.values.astype(int)

data_length = len(data)
data_width = len(data[0])

while True:

    num_rooms = teacher_num_rooms(data)
    print(list(num_rooms.values()))

    for _ in range(20000):
        rand_row1 = random.randint(0, data_length - 1)
        rand_row2 = random.choice(
            list(set([x for x in range(0, data_length - 1)]) - set([rand_row1])))
        rand_col = random.randint(0, data_width - 1)

        num_rooms = teacher_num_rooms(data)
        noct, error = calc_fitness_values(num_rooms)
        fitness = noct * 1 - error * 6

        data[rand_row1][rand_col], data[rand_row2][rand_col] = data[rand_row2][rand_col], data[rand_row1][rand_col]

        num_rooms = teacher_num_rooms(data)
        noct, error = calc_fitness_values(num_rooms)
        new_fitness = noct * 1 - error * 6

        if new_fitness < fitness:
            data[rand_row1][rand_col], data[rand_row2][rand_col] = data[rand_row2][rand_col], data[rand_row1][rand_col]

    x = input()
    if x == 'q':
        break

new_data_frame = pd.DataFrame(data, index=periods, columns=classrooms)
new_data_frame.replace(0, np.nan, inplace=True)
new_data_frame.to_excel('new_data.xlsx')