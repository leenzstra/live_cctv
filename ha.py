import numpy as np

h = 300
w = 300
mWH = 2
output = np.zeros((h * mWH, w * mWH, 3), dtype="uint8")

cur_row = 0
cur_col = 0
d = {1:1, 2:2, 3:3}
for (k, f) in d.items():
    print(cur_row, cur_col)
    output[cur_row*h: h*(cur_row+1), cur_col*w: w*(cur_col+1)] = f

    cur_col += 1
    cur_col %= mWH

    if (cur_col == 0):
        cur_row += 1
