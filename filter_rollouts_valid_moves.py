import csv
import logging
import numpy as np

logging.getLogger().setLevel(logging.INFO)

rows=[]
row_buf=[]

with open('rollouts-valid-moves.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        # print(str(len(row)))
        assert(len(row) == 91)
        if 0 in row[84:91]:
            # if len(row_buf) > 0:
            #     rows.append(row_buf[len(row_buf)-1])
            rows.append(row)
            row_buf=[]
        else:
            row_buf.append(row)

with open('rollouts-valid-moves-filtered.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)