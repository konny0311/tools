import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('', names=['num1', 'num2'])
plt.plot(range(0,10),df['num2'],marker="o")
plt.show()