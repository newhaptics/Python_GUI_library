# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:55:41 2020

@author: NewHaptics01
"""


def myfunc(s):
    for letter in s:
        if s.index(letter) % 2 == 0:
            letter = letter.upper()
    return s

myfunc('hello')
