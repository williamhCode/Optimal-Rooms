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

    num_rooms = dict(sorted(num_rooms.items()))

    return num_rooms


def calc_fitness_values(num_rooms):
    num_one_classroom_teachers = list(num_rooms.values()).count(1)

    error = 0
    for value in num_rooms.values():
        error += (value - 1)**2
    error /= len(num_rooms)

    return num_one_classroom_teachers, error


def data_to_analysis_dict(data):
    analysis_dict = defaultdict(lambda: defaultdict(list))

    for j in range(len(data[0])):
        for i in range(len(data)):
            value = data[i][j]
            if value == 0:
                continue
            analysis_dict[value][i].append(j)

    for key, value in analysis_dict.items():
        analysis_dict[key] = dict(sorted(value.items()))

    analysis_dict = dict(sorted(analysis_dict.items()))

    return analysis_dict


data_frame: pd.DataFrame = pd.read_excel('data.xlsx', index_col=0)

periods: np.ndarray = data_frame.index.values.astype(int)
classrooms: np.ndarray = data_frame.columns.values.astype(str)

data = data_frame.values.astype(int)
old_data = data

while True:
    num_rooms = teacher_num_rooms(data)
    print(list(num_rooms.values()))
    analysis_dict = data_to_analysis_dict(data)

    mx = max(num_rooms.values())
    max_vals = [k for k, v in num_rooms.items() if v == mx]
    random.shuffle(max_vals)

    for key in max_vals:
        row_col = analysis_dict[key]
        min_row = min(row_col, key=lambda k: len(row_col.get(k)))
        max_row = max(row_col, key=lambda k: len(row_col.get(k)))

        for j in row_col[min_row]:
            noct, error = calc_fitness_values(num_rooms)
            fitness = noct * 1 - error * 5

            data[min_row][j], data[max_row][j] = data[max_row][j], data[min_row][j]

            num_rooms = teacher_num_rooms(data)
            noct, error = calc_fitness_values(num_rooms)
            new_fitness = noct * 1 - error * 5

            if new_fitness < fitness:
                data[min_row][j], data[max_row][j] = data[max_row][j], data[min_row][j]

    input()