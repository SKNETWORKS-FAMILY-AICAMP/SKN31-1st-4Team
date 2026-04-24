import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Car_info = pd.read_csv("./csv/encar_cars_v2.csv")

print(Car_info.shape())

print(Car_info.head())