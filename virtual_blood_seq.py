# -*- coding: utf-8 -*-

import sys
import time
import numpy as np
import pandas as pd
from random import randint
from datetime import timedelta
from random_vector import RandFloats, RandIntVec
from multiprocessing.dummy import Pool as ThreadPool

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

def get_columns(df):
  columns_list = []
  for col_name, col_data in df.iloc[:, 1:].iteritems():
    col_list = [col_name, col_data]
    columns_list.append(col_list)
  return columns_list

def random_df(seq_list, n):
  col_name = seq_list[0]
  col_data = seq_list[1]
  data = col_data.to_numpy()
  arr = random_n_partition(data, n)
  randarr = random_array(arr)
  return pd.DataFrame(randarr, columns=columns_name(str(col_name), n))

def main():
  number2split = 10
  dataframe = read_data(sys.argv[1])
  columns_list = get_columns(dataframe)
  n_list = [number2split for _ in range(number2split)]

  pool = ThreadPool(4)
  results = pool.starmap(random_df, zip(columns_list, n_list))

  # Close the pool and wait for the work to finish
  pool.close()
  pool.join()

  results_df = pd.concat(results, axis=1)
  results_df = pd.concat([dataframe, results_df], axis=1)
  results_df.to_excel('virtual_seq.xlsx', index=False)

if __name__ == "__main__":
  start_time = time.time()
  main()
  print("--- %s seconds ---" % str(timedelta(seconds=time.time()-start_time)))
