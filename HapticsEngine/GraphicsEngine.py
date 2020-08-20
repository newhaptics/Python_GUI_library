# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:18:00 2020

@author: Derek Joslin
"""

""" this class performs operations on a matrix and changes the values inside """

import numpy as np
import cairo as ca
import math



class GraphicsEngine:
    
    def __init__(self,matrix):
        #create the graphics
        self.__data = np.array(matrix).astype(dtype=np.uint8)
        self.__data[self.__data == 1] = 255
        dim = self.__data.shape
        self.state = matrix
        surface = ca.ImageSurface.create_for_data(self.__data, ca.FORMAT_A8, dim[0], dim[1])
        self.__ct = ca.Context(surface)
        self.__ct.set_operator(ca.OPERATOR_SOURCE)
        self.__output = 1
    
    def read_matrix(self, matrix):
        #create the graphics
        self.__data = np.array(matrix).astype(dtype=np.uint8)
        self.__data[self.__data == 1] = 255
        dim = self.__data.shape
        self.state = matrix
        surface = ca.ImageSurface.create_for_data(self.__data, ca.FORMAT_A8, dim[0], dim[1])
        self.__ct = ca.Context(surface)
        
    
    def set_output(self,val):
        """ sets the output value of all pycairo commands """
        self.__output = val
        
        
    def select_element(self,coord):
        if self.__output:
            self.__data[coord[0], coord[1]] = 255    
        else:
            self.__data[coord[0],coord[1]] = 0
        
        self.state[coord[0]][coord[1]] = self.__output
    
    
    
    def make_line(self, start, end, width):
        """ takes in two tuples that represent coordinates of the 
        start and end locations of the line """
        #use offset if width is odd
        if (width % 2) == 0:
            offset = 0
        else:
            offset = 0.5
                
        #add .5 to the start and end
        startX = start[0] + offset
        startY = start[1] + offset
        endX = end[0] + offset
        endY = end[1] + offset
        self.__ct.move_to(startX,startY)
        self.__ct.line_to(endX,endY)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        self.__ct.stroke()
        self.__save_data()
        
        
    def make_bezierCurve(self, start, c1, c2, end, width):
        startX = start[0]
        startY = start[1]
        endX = end[0]
        endY = end[1]
        self.__ct.move_to(startX,startY)
        self.__ct.curve_to(c1[0], c1[1], c2[0], c2[1], endX, endY)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        self.__ct.stroke()
        self.__save_data()
        
    def make_circle(self, center, radius, width, fill):
        """ take in a center and radius and fill or stroke depending on selection"""
        self.__ct.arc(center[0], center[1], radius, 0, 2*math.pi)
        self.__ct.set_line_width(width)
        if fill:
            self.__ct.fill()
        else:
            self.__ct.stroke()
        self.__save_data()
        
        
        
    def make_polgon(self, start, points, width, fill):
        startX = start[0]
        startY = start[1]
        self.__ct.move_to(startX,startY)
        for point in points:
            self.__ct.line_to(point[0],point[1])
        self.__ct.line_to(startX, startY)    
        
        self.__ct.set_line_width(width)
        if fill:
            self.__ct.fill()
        else:
            self.__ct.stroke()
        self.__save_data()
            
        
        
    def make_rectangle(self, corner1, corner2, width, fill):
        startX = corner1[0]
        startY = corner1[1]
        endX = corner2[0]
        endY = corner2[1]
        X1 = endX - startX
        Y1 = startY
        X2 = startX - endY
        Y2 = endY
        self.__ct.move_to(startX,startY)
        self.__ct.line_to(X1,Y1)
        self.__ct.line_to(endX,endY)
        self.__ct.line_to(X2,Y2)
        self.__ct.set_line_width(width)
        if fill:
            self.__ct.fill()
        else:
            self.__ct.stroke()
        self.__save_data()
        
    def __save_data(self):
        print('---------------------------\n\r')
        print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
                         for row in self.__data.tolist()]))
        self.__data[self.__data > 115] = 255
        self.__data[self.__data != 255] = 0
        self.state.clear()
        self.state.extend((self.__data == 255).tolist())
        
        
        
        
        
        
data = np.zeros((20,20), dtype=np.uint8)
data = data.tolist()
ge = GraphicsEngine(data)
ge.set_output(1)
ge.make_rectangle((5,5), (15,15), 1, 0)
#ge.make_polgon((5,5), [(7,8),(3,12)], 1, 0)

#ge.make_bezierCurve((1,1), (14,3), (4,10), (18,20), 3)
# =============================================================================
# ge.make_circle((10,10), 9.5, 2, 1)
# ge.make_line((19,0),(0,19), 1)
# ge.make_line((5,20),(20,0), 1)
# ge.make_line((5,0),(5,20), 1)
# ge.make_line((0,5),(20,5), 2)
# ge.set_output(0)
# ge.make_line((8,0),(8,20), 5)
# ge.make_line((0,8),(20,8), 5)
# ge.select_element((5,3))
# =============================================================================

# write output
print('---------------------------\n\r')
print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
         for row in data]))
