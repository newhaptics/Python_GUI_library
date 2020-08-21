# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 16:40:00 2020

@author: Derek Joslin
"""

import HapticsEngine as he
import HapticVisualizer as hv
import time

#Matrices to transform
startMatrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]]

endMatrix = [[1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, ],
             [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
             [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, ],
             [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, ],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
             [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, ],
             [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, ],
             [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, ],
             [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, ],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1 ]]

#timing matrices
ts = [[20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, 40, ],
      [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 20, ]]

th = [[10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ],
      [10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, 10, 30, 30, 30, ],
      [10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, 10, 80, 80, 80, ]]

tpw = [[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ],
       [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ]]

def display_matrix(matrix,number):
    print(chr(27) + "[2J")
    print('time: {0}'.format(number))
    print('---------------------------\n\r')
    print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                 for row in matrix]))

def display_refresh():
    elapsed_time = 0
    for now in times:
        while elapsed_time != now:
            elapsed_time = round((time.perf_counter() - clock2)*1000)
        else:
            engine.set_stateTime(now)
            display_matrix(engine.get_currentState(), now)
    

engine = he.HapticsEngine(tpw,th,ts, 20, 20, 'row by row')
engine.ge.write_braille((3,12), "hello \n world")
engine.ge.make_circle((10,10), 10, 1, 0)
display_matrix(engine.get_desiredState(), 0)
#engine.set_desiredState(endMatrix)

clock1 = time.perf_counter()
times = engine.generate_refreshStates()
clock1 = time.perf_counter() - clock1


clock2 = time.perf_counter()
display_refresh()
clock2 = time.perf_counter() - clock2

print(clock1)
print(clock2)