# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from random_vector import RandFloats, RandIntVec

def read_data(filename, col):
  df = pd.read_excel(filename, header=0)
  return df.iloc[:, col]

def random_n_partition(data, n):
  rdarr = []
  for value in data:
    list_size = 10
    list_sum_value = value
    rdpt = RandIntVec(list_size, list_sum_value, RandFloats(list_size))
    rdarr.extend(rdpt)
  arr = np.array(rdarr).reshape((len(rdarr)//list_size, list_size))
  df = pd.DataFrame(arr)
  df.to_csv('virtual_seq.csv')

def main():
  data = read_data(sys.argv[1], 2).tolist()
  random_n_partition(data, 10)

if __name__ == "__main__":
  main()
