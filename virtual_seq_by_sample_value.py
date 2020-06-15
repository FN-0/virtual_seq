# -*- coding: utf-8 -*-

import sys
import time
import random
import numpy as np
import pandas as pd
from random import randint
from datetime import timedelta
from random_vector import RandFloats, RandIntVec
from multiprocessing.dummy import Pool as ThreadPool

def read_data(filename):
  df = pd.read_csv(filename, header=0, index_col='name')
  print('Read data ok')
  return df

def columns_name(col_name, n):
  return [("%s_%05d" % (col_name, n))]

def get_max_min(df):
  return [df.max(axis=1), df.min(axis=1)]

def random_df(df, n):
  df_max, df_min = get_max_min(df)
  col_name = 'sample'
  rdar = []
  for maxn, minn in zip(df_max, df_min):
    gap = maxn - minn
    rn = minn + random.randint(0, gap)
    rdar.append(rn)
  return pd.DataFrame(rdar, columns=columns_name(str(col_name), n), index=df.index)

def main():
  number2generate = 10
  dataframe = read_data(sys.argv[1]).fillna(0)
  
  #pool = ThreadPool(20)
  results = []
  for i in range(number2generate):
    results.append(random_df(dataframe, i))

  # Close the pool and wait for the work to finish
  #pool.close()
  #pool.join()

  results_df = pd.concat(results, axis=1)
  #results_df = pd.concat([dataframe, results_df], axis=1)
  t = time.strftime("%Y%m%d%H%M%S", time.localtime())
  results_df.to_csv('output/virtual_seq_%s.csv' % t)

if __name__ == "__main__":
  start_time = time.time()
  main()
  print("--- %s seconds ---" % str(timedelta(seconds=time.time()-start_time)))
