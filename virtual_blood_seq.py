# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from random import randint
from random_vector import RandFloats, RandIntVec

def read_data(filename, col=-1):
  df = pd.read_excel(filename, header=0)
  print('Read data ok')
  if col == -1:
    return df
  return df.iloc[:, 0:col]

def generate_random_list(list_size, list_sum_value, value):
  while(True):
    rdpt = RandIntVec(list_size, list_sum_value, RandFloats(list_size))
    if check_std(rdpt, list_sum_value):
      return rdpt

def check_std(lst, list_sum_value):
  if list_sum_value > 1000:
    lst = np.array(lst)/list_sum_value*1000
  stdv = np.std(lst)
  if stdv < 30:
    return True
  else:
    return False

def random_n_partition(data, n):
  rdarr = []
  for value in data:
    list_size = n
    list_sum_value = value
    rdpt = generate_random_list(list_size, list_sum_value, value)
    rdarr.extend(rdpt)
  arr = n * np.array(rdarr).reshape((len(rdarr)//list_size, list_size))
  return arr

def random_shift(n):
  n += randint(-9, 9)
  if n <= 10:
    return 0
  return n

def random_array(arr):
  rows, cols = arr.shape
  for i in range(rows):
    for j in range(cols):
      arr[i][j] = random_shift(arr[i][j])
  return arr

def columns_name(col_name, n):
  return [("%s_%05d" % (col_name, n)) for n in range(n)]

def main():
  number2split = 5
  dataframe = read_data(sys.argv[1])
  #vts = pd.DataFrame()
  for col_name, col_data in dataframe.iloc[:, 1:].iteritems():
    #print(columns_name(str(col_name), number2split))
    data = col_data.to_numpy()
    arr = random_n_partition(data, number2split)
    randarr = random_array(arr)
    df = pd.DataFrame(randarr, columns=columns_name(str(col_name), number2split))
    dataframe = pd.concat([dataframe, df], axis=1)
  dataframe.to_excel('virtual_seq.xlsx', index=False)

if __name__ == "__main__":
  main()
