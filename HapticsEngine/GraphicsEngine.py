# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 10:18:00 2020

@author: Derek Joslin
"""

""" this class performs operations on a matrix and changes the values inside """

import numpy as np
import cairo as ca
import time
import math

class GraphicsEngine:

    def __init__(self,matrix):
        #create the graphics
        #first figure out the dimensions of the given matrix
        newMat = np.array(matrix)
        dim = newMat.shape
        newDim = (math.ceil(dim[0]/20)*20, math.ceil(dim[1]/20)*20)
        self.__data = np.zeros((newDim[0],newDim[1]), dtype=np.uint8)
        self.__oldDim = dim
        #copy data from the input matrix to internal data
        self.__data[0:dim[0],0:dim[1]] = newMat
        self.__data[self.__data == 1] = 255
        self.state = matrix
        surface = ca.ImageSurface.create_for_data(self.__data, ca.FORMAT_A8, newDim[0], newDim[1])
        self.__ct = ca.Context(surface)
        self.__ct.set_operator(ca.OPERATOR_SOURCE)
        self.__output = True

    def read_matrix(self, matrix):
        #create the graphics
        #first figure out the dimensions of the given matrix
        newMat = np.array(matrix)
        dim = newMat.shape
        newDim = (math.ceil(dim[0]/20)*20, math.ceil(dim[1]/20)*20)
        self.__data = np.zeros((newDim[0],newDim[1]), dtype=np.uint8)
        self.__oldDim = dim
        #copy data from the input matrix to internal data
        self.__data[0:dim[0],0:dim[1]] = newMat
        self.__data[self.__data == 1] = 255
        dim = self.__data.shape
        self.state = matrix
        surface = ca.ImageSurface.create_for_data(self.__data, ca.FORMAT_A8, newDim[0], newDim[1])
        self.__ct = ca.Context(surface)


    def set_output(self,val):
        """ sets the output value of all pycairo commands """
        self.__output = val


    def select_element(self,coord):
        """ selects a single element to change """
        if self.__output:
            self.__data[coord[0], coord[1]] = 255
        else:
            self.__data[coord[0], coord[1]] = 0

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
        startY = start[0] + offset
        startX = start[1] + offset
        endY = end[0] + offset
        endX = end[1] + offset
        self.__ct.move_to(startX,startY)
        self.__ct.line_to(endX,endY)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        self.__ct.stroke()
        self.__save_data()


    def make_bezierCurve(self, start, c1, c2, end, width):
        """ takes in a start point and end point as well as two curve points
        it produces a line that bends to all the points """
        startY = start[0]
        startX = start[1]
        endY = end[0]
        endX = end[1]
        self.__ct.move_to(startX,startY)
        self.__ct.curve_to(c1[1], c1[0], c2[1], c2[0], endX, endY)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        self.__ct.stroke()
        self.__save_data()

    def make_circle(self, center, radius, width, fill):
        """ take in a center and radius and fill or stroke depending on selection"""
        self.__ct.arc(center[1], center[0], radius, 0, 2*math.pi)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        if fill:
            self.__ct.fill()
        else:
            self.__ct.stroke()
        self.__save_data()



    def make_polygon(self, start, points, width, fill):
        """ take in multiple points and string them all together """
        #use offset if width is odd
        if (width % 2) == 0:
            offset = 0
        else:
            offset = 0.5

        startY = start[0] + offset
        startX = start[1] + offset

        self.__ct.move_to(startX,startY)
        for point in points:
            self.__ct.line_to(point[1] + offset, point[0] + offset)
        self.__ct.line_to(startX, startY)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        if fill:
            self.__ct.fill()
        else:
            self.__ct.stroke()
        self.__save_data()



    def make_rectangle(self, corner1, corner2, width, fill):
        """ take in two corners of a rectangle and string together to make the correct shape """
        #use offset if width is odd
        if (width % 2) == 0:
            offset = 0
        else:
            offset = 0.5

        startY = corner1[0] + offset
        startX = corner1[1] + offset
        endY = corner2[0] + offset
        endX = corner2[1] + offset
        X1 = endX
        Y1 = startY
        X2 = startX
        Y2 = endY
        self.__ct.move_to(startX,startY)
        self.__ct.line_to(X1,Y1)
        self.__ct.line_to(endX,endY)
        self.__ct.line_to(X2,Y2)
        self.__ct.line_to(startX,startY)
        self.__ct.set_line_width(width)
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        if fill:
            self.__ct.fill()
        else:
            self.__ct.stroke()
        self.__save_data()

    def write_latin(self, start, displayString, font, size):
        """ takes in starting point for font and string to write
        naturally fills up the screen as you type """
        startY = start[0]
        startX = start[1]
        #move to start point
        self.__ct.move_to(startX,startY)

        #select the braille font
        self.__ct.select_font_face(font, ca.FONT_SLANT_NORMAL, ca.FONT_WEIGHT_BOLD)
        self.__ct.set_font_size(size)


        #type out the text
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        self.__ct.show_text(displayString)
        self.__save_data()

    def write_braille(self, start, brailleString):
        """ takes in starting point for font and string to write
        naturally fills up the screen as you type """
        startY = start[0]
        startX = start[1] + 3
        #move to start point
        self.__ct.move_to(startX,startY)

        #select the braille font
        self.__ct.select_font_face("Braille", ca.FONT_SLANT_NORMAL, ca.FONT_WEIGHT_NORMAL)
        self.__ct.set_font_size(3)


        #type out the text
        self.__ct.set_source_rgba(self.__output, self.__output, self.__output, self.__output)
        #xy locations of typing the letters and dimensions to know where to stop
        x = startX
        y = startY
        dim = self.__oldDim
        dimX = dim[0]
        dimY = dim[1]
        for letter in brailleString:
            if letter == '\n':
                if y + 4 < dimY:
                    x = 0
                    y = y + 4
                else:
                    break
            else:
                self.__ct.show_text(letter)
                if (letter.isupper() or letter.isdigit()) and x + 5 < dimX:
                    x = x + 5
                elif not (letter.isupper() or letter.isdigit()) and x + 3 < dimX:  #if the letter is a lower case make room plus a space
                    x = x + 3
                elif y + 4 < dimY: #if the end of the line is reached start a new line
                    y = y + 3
                    x = 0
                else: #end of the string
                    break
            self.__ct.move_to(x,y)
        self.__save_data()


    def clear(self):
        self.__data[:,:] = 0
        self.__save_data()

    def __save_data(self):
        #print('---------------------------\n\r')
        #print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
        # for row in self.__data]))
        self.__data[self.__data > 115] = 255
        self.__data[self.__data != 255] = 0
        dim = np.array(self.state).shape
        self.state.clear()
        self.state.extend((self.__data[0:dim[0],0:dim[1]] == 255).tolist())






# =============================================================================
# data = np.zeros((14,15), dtype=np.uint8)
# data = data.tolist()
# ge = GraphicsEngine(data)
# ge.set_output(1)
# for word in ["Hello", "World", "th1s", "!s", "deRek"]:
#     ge.set_output(1)
#     ge.write_braille((2,14), word)
#     time.sleep(1)
#     print('---------------------------\n\r')
#     print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
#                      for row in data]))
#     ge.clear()
# =============================================================================

#ge.make_rectangle((4,4), (8,8), 1, 0)
#ge.make_polgon((0,0), [(0,19),(19,9)], 1, 1)

#ge.make_bezierCurve((1,1), (14,3), (4,10), (18,20), 3)
#ge.make_circle((7,7), 7, 1, 0)
#ge.make_line((0,0),(15,14), 1)
#ge.make_line((5,20),(20,0), 1)
#ge.make_line((5,0),(5,20), 1)
#ge.make_line((0,5),(20,5), 2)
#ge.set_output(0)
#ge.make_line((8,0),(8,20), 5)
#ge.make_line((0,8),(20,8), 5)
#ge.select_element((5,3))

# write output
# =============================================================================
# print('---------------------------\n\r')
# print('\n'.join([' '.join(['{:4}'.format(item) for item in row])
#          for row in data]))
# =============================================================================
