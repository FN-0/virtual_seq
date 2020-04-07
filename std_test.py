# -*- coding: utf-8 -*-

import numpy as np
from random_vector import RandFloats, RandIntVec

def main():
  list_size = 10
  list_sum_value = 10000
  while(True):
    rdpt = RandIntVec(list_size, list_sum_value, RandFloats(list_size))
    stdv = np.std(np.array(rdpt)/list_sum_value*1000)
    if stdv < 30:
      print(rdpt, stdv)
      input()

if __name__ == "__main__":
  main()