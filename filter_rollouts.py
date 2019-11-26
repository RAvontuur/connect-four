import csv
import logging
import numpy as np

logging.getLogger().setLevel(logging.INFO)

rows=[]
row_buf=[]

with open('rollouts.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        if row[0] + row[1] > 0.5:
            rows.append(row_buf[np.random.randint(len(row_buf)-1, size=1)[0]])
            rows.append(row_buf[-1])
            rows.append(row)
        else:
            row_buf.append(row)

with open('rollouts-filtered.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)