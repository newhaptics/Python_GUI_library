# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 12:21:28 2020

@author: NewHaptics01
"""


#quick array generator
print('[', end = '')
for x in range(0,14):
    print('[', end = '')
    for y in range(0,15):
        if y == x:
            print('0, ', end = '')
        else:
            print('0, ', end = '')
    print('],')
print(']')