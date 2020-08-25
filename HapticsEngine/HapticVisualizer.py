# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:43:30 2020

@author: Derek Joslin
"""

import sys
import HapticsEngine as he
import time

from qtpy.QtWidgets import QApplication
from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl


#timing matrices
ts = [[1000 for i in range(0,20)] for j in range(0,20)]

th = [[2000 for i in range(0,20)] for j in range(0,20)]

tpw = [[1000 for i in range(0,20)] for j in range(0,20)]


#create the backend haptics engine
engine = he.HapticsEngine(tpw,th,ts, 15, 14, 'row by row')
full = 0
width = 1
times = 0


def display_matrix(matrix,number):
    print('time: {0}'.format(number))
    print('---------------------------\n')
    print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                 for row in matrix]))
    print('---------------------------\n')

def erase(onOff):
    if onOff == "on":
        engine.ge.set_output(0)
    else:
        engine.ge.set_output(1)

def fill(onOff):
    global full
    if onOff == "on":
        full = 1
    else:
        full = 0

def stroke(size):
    global width
    width = size

def dot(coord):
    engine.ge.select_element(coord)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def line(start, end):
    engine.ge.make_line(start, end, width)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def curve(start, control1, control2, end):
    engine.ge.make_bezierCurve(start, control1, control2, end, width)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def circle(center, radius):
    engine.ge.make_circle(center, radius, width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def rect(corner1, corner2):
    engine.ge.make_rectangle(corner1, corner2, width)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def triangle(point1, point2, point3):
    engine.ge.make_polygon(point1, [point2, point3], width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def polygon(points):
    engine.ge.make_polygon(points[0], points[1:-1], width, full)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    
def braille(point, text):
    engine.ge.write_braille(point, text)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    
def latin(point, text, font, size):
    engine.ge.write_latin(point, text, font, size)
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)
    
def clear():
    engine.ge.clear()
    print("desired state \n")
    display_matrix(engine.get_desiredState(), 0)

def state():
    print("desired state \n")
    display_matrix(engine.get_currentState(), 0)

def refresh():
    global times
    times = engine.generate_refreshStates()
    clock2 = time.perf_counter()
    elapsed_time = 0
    for now in times:
        while elapsed_time != now:
            elapsed_time = round((time.perf_counter() - clock2)*1000)
        else:
            engine.set_stateTime(now)
            display_matrix(engine.get_currentState(), now)
    clock2 = time.perf_counter() - clock2
    print(clock2)
    if engine.check_connection():
        engine.send_toBoard()
    
def times(now):
    engine.set_stateTime(now)
    display_matrix(engine.get_currentState(), now)
    if engine.check_connection():
        engine.send_toBoard()

def frames():
    print(times)
    
def connect(COM):
    engine.establish_connection(COM)
    
def disconnect():
    engine.end_connection()
    

if __name__ == '__main__':
    app = QApplication([])

    #console creation
    console = PythonConsole(formats={
    'keyword':    hl.format('blue', 'bold'),
    'operator':   hl.format('red'),
    'brace':      hl.format('darkGray'),
    'defclass':   hl.format('black', 'bold'),
    'string':     hl.format('magenta'),
    'string2':    hl.format('darkMagenta'),
    'comment':    hl.format('darkGreen', 'italic'),
    'self':       hl.format('black', 'italic'),
    'numbers':    hl.format('brown'),
    'inprompt':   hl.format('darkBlue', 'bold'),
    'outprompt':  hl.format('darkRed', 'bold'),
    })


    #add all the functions of the program
    console.push_local_ns('erase', erase)
    console.push_local_ns('fill', fill)
    console.push_local_ns('stroke', stroke)
    console.push_local_ns('dot', dot)
    console.push_local_ns('line', line)
    console.push_local_ns('curve', curve)
    console.push_local_ns('circle', circle)
    console.push_local_ns('rect', rect)
    console.push_local_ns('triangle', triangle)
    console.push_local_ns('polygon', polygon)
    console.push_local_ns('latin', latin)
    console.push_local_ns('braille', braille)
    console.push_local_ns('clear', clear)
    console.push_local_ns('state', state)
    console.push_local_ns('refresh', refresh)
    console.push_local_ns('times', times)
    console.push_local_ns('frames', frames)
    console.push_local_ns('connect', connect)
    console.push_local_ns('disconnect', disconnect)
    
    

    console.show()

    console.eval_queued()

    sys.exit(app.exec_())
