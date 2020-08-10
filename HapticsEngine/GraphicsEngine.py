# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:18:00 2020

@author: Derek Joslin
"""

""" this class performs operations on a matrix and changes the values inside """

# =============================================================================
# import numpy as np
# 
# 
# class GraphicsEngine:
#     
#     def __init__(self):
#         #create the graphics
#         
#     def fill_matrix(startMatrix):
#         """ takes in a matrix to edit and returns edited matrix """
#         
#         
#         
# =============================================================================

import numpy
import cairo
import math

data = numpy.zeros((200, 200, 4), dtype=numpy.uint8)
surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, 200, 200)
cr = cairo.Context(surface)

# fill with solid white
cr.set_source_rgb(1.0, 1.0, 1.0)
cr.paint()

# draw red circle
cr.arc(100, 100, 80, 0, 2*math.pi)
cr.set_line_width(3)
cr.set_source_rgb(1.0, 0.0, 0.0)
cr.stroke()

data = data.tolist()

# write output
print (data)
surface.write_to_png("circle.png")