#!/usr/local/bin/python3
# encoding: utf-8
# -*- coding: utf8 -*-
#FIBONACII

i = 1
j = 1
print(f'{i}\n{j}')
for loop in range(1000):
    k = i + j
    i,j = j,k
    # print(f'this {loop} fibonacci is {k}')
    print(f'{k}')
