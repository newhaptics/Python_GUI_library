# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 12:21:28 2020

@author: NewHaptics01
"""


#quick array generator
print('[', end = '')
for x in range(0,20):
    print('[', end = '')
    for y in range(0,20):
        if y == x:
            print('1000, ', end = '')
        else:
            print('1000, ', end = '')
    print('],')
print(']')