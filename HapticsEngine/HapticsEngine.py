# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 12:25:03 2020

@author: Derek Joslin
"""

import TactileTweener


class HapticsEngine:

    #haptics engine takes in physics of a board and properly executes graphical commands based on the physics
    #take in the physics of the fluidic chip from matlab and use that to determine timing for actions
    #maybe have it take in an FC library class
    
    def __init__(self, tpw, th, ts, rows, columns, refreshProtocol):
        self.__tpw = tpw
        self.__th = th
        self.__ts = ts
        self.__rows = rows
        self.__columns = columns
        self.__currentState = [[0] * columns] * rows
        self.__desiredState = [[0] * columns] * rows
        self.__refreshInfo = {'refresh protocol': refreshProtocol}
        #calculate how fast each element in the chip updates based on the setup, hold, and pulse width of the element
        elementTiming = th + ts  
        elementTiming = [tpw for element in [row for row in elementTiming] if tpw > th]
        self.__refreshInfo.update({'element refresh timing' : elementTiming})
        
    def get_state(self):
        return self.__currentState
    
    #returns dictionary with all important transformation info
    def get_refreshInfo(self):
        return self.__refreshInfo
    
    #creates the frames and to get from current state to desired state
    def refresh_chip(self,protocol):
        #create a tweener to get the frames to get to the desired state
        tt = TactileTweener()
        
        #tween the frames 
        refreshFrames = tt.get_tweenFrames(self.__currentState, self.__desiredState, self.__refreshInfo['refresh protocol'])
        
        #set the current time to 0
        currentTime = 0
        
        #calculate the time when each element will refresh for each frame
        elementTiming = self.__refreshInfo['element refresh timing']
        timeMatrix = [[currentTime] * self.__columns] * self.__rows
        
        for index, frame in enumerate(refreshFrames):
            for rowIndex, row in enumerate(frame['change time']):
                for columnIndex, elementChange in enumerate(frame['change time']):
                    if elementChange == True:
                        timeMatrix[rowIndex][columnIndex] += elementTiming[rowIndex][columnIndex]
            refreshFrames[index].update({'timing data': timeMatrix})
        
        self.__refreshInfo.update({'frame info': refreshFrames})
        
        
   
    def set_refreshProtocol(self,protocol):
        self.__refreshInfo['refresh protocol'] = protocol
        
        
    #move one frame forward in the fluidic chip state
    def set_time(self):
        #give the state at the inputed time
        x = 0
        refreshFrames = self.__refreshInfo['frame info']
        for frame in refreshFrames:
            print('frame: {0}'.format(x))
        x += 1
        print('---------------------------\n\r')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in frame['state']]))
        print('T/F')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in frame['element change']]))
        print('timing data')
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in frame['timing data']]))
        