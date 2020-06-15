# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
import numpy as np
import pandas as pd

def find_n_nonzero_row(df):
  n_nonzero_row_list = []
  for label, row in df.iterrows():
    protein_array = np.array(row.to_list())
    if np.sum(protein_array) < 10000:
      n_nonzero_row_list.append(label)
  return n_nonzero_row_list

def remove_confirm(len_index, len_n_nonzero_row_list):
  print('Length of rest of gene: ', len_index-len_n_nonzero_row_list)
  '''remove_conf = input('Remove? y/n ')
  if remove_conf == 'y':
    return True
  elif remove_conf == 'n':
    pass
  else:
    print('Usage: input y or n.')
  return False'''
  return True

def remove_row(df, n_nonzero_row_list):
  return df.drop(n_nonzero_row_list)

def main():
  df = pd.read_csv(sys.argv[1], index_col='name')
  n_nonzero_row_list = find_n_nonzero_row(df)
  print(len(n_nonzero_row_list))
  df = remove_row(df, n_nonzero_row_list)
  df.to_csv(os.path.basename(sys.argv[1]).split('.')[0]+'_.csv')

if __name__ == "__main__":
  main()
