import matplotlib.pyplot as plt
import csv
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument('--csv',help='input csv file path')
args = parser.parse_args()

if not args.csv:
    print('missing csv file path')
    exit()
else:
    x = []
    y = []
    with open(args.csv, 'r') as f:
        rows = csv.reader(f, delimiter=',')
        x = next(rows)
        x = np.array(x[1:])
        for row in rows:
            row_int = []
            for num in row[1:]:
                row_int.append(float(num))
            y.append(np.array(row_int))
    fig, ax = plt.subplots()
    ax.plot(x, y[0], label='train=4137')
    ax.plot(x, y[1], label='train=8275')
    ax.plot(x, y[2], label='train=16551')
    ax.tick_params(length = 5, colors = "black")
    ax.set_xlabel('classes')
    ax.set_ylabel('AP')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=20, fontsize=10);
    plt.legend()
    plt.savefig('test.jpg')

