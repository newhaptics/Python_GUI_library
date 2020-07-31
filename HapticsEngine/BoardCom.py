# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:39:32 2020

@author: Derek Joslin
"""


class BoardCom:
    
     #the haptics engine contains a serial port connection object


    def __init__(self,port):
        self.__port = serial.Serial(port, 115200, timeout=1)

    #Display the supported commands.
    def help(self):
        self.__port.write('HELP\n'.encode('utf-8'))
        print(self.__read_rx())

    #Reset the controller board.
    def reset(self):
        self.__port.write('RESET\n'.encode('utf-8'))
        print(self.__read_rx())

    #Display the Firmware Version.
    def version(self):
        self.__port.write('VERSION\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the size of the fluidic chip array as m (rows) n (cols). Example: SETSIZE 3 4
    def set_size(self,rows,columns):
        self.__port.write('SETSIZE {0} {1}\n'.format(rows,columns).encode('utf-8'))
        print(self.__read_rx())

    #Display the current size of the fluidic chip array.
    def get_size(self):
        self.__port.write('GETSIZE\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the timing parameters for the solenoids as t_s t_pw t_ph (ms). Example: SETTIMES 25 35 45
    def set_times(self,ts,tpw,tph):
        self.__port.write('SETTIMES {0} {1} {2}\n'.format(ts,tpw,tph).encode('utf-8'))
        print(self.__read_rx())

    #Display the current timing parameters for the solenoids.
    def get_times(self):
        self.__port.write('GETTIMES\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the row starting index and step size as r (row index) s (step size). Example SETROW 0 1
    def set_row(self,rowIndex,step):
        self.__port.write('SETROW {0} {1}\n'.format(rowIndex,step).encode('utf-8'))
        print(self.__read_rx())

    #Display the current row starting index and step size
    def get_row(self):
        self.__port.write('GETROW\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the column starting index and step size as c (column index) s (step size). Example: SETCOL 3 1
    def set_col(self,columnIndex,step):
        self.__port.write('SETCOL {0} {1}\n'.format(columnIndex,step).encode('utf-8'))
        print(self.__read_rx())

    #Display the current column starting index and step size.
    def get_col(self):
        self.__port.write('GETCOL\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the trigger index as t (trigger index). Example: SETTRIG 60
    def set_trig(self,tIndex):
        self.__port.write('SETTRIG {0}\n'.format(tIndex).encode('utf-8'))
        print(self.__read_rx())

    #Display the current trigger index.
    def get_trig(self):
        self.__port.write('GETTRIG\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the source index as s (source index). Example: SETSOURCE 61
    def set_source(self,sIndex):
        self.__port.write('SETSOURCE {0}\n'.format(sIndex).encode('utf-8'))
        print(self.__read_rx())

    #Display the current source index.
    def get_source(self):
        self.__port.write('GETSOURCE\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the states for the solenoids in the matrix. Example: SETMATRIX A1B4 C39F 56A
    def set_matrix(self,mat):
        self.__port.write('SETMATRIX'.encode('utf-8'))
        #write each matrix row
        for row in mat:
            self.__port.write(' {0}'.format(row).encode('utf-8'))
        self.__port.write('\n'.encode('utf-8'))
        print(self.__read_rx())

    #Get the states for the solenoids in the matrix.
    def get_matrix(self):
        self.__port.write('GETMATRIX\n'.encode('utf-8'))
        print(self.__read_rx())

    #Start solenoids operating by turning on Source.
    def start(self):
        self.__port.write('START\n'.encode('utf-8'))
        print(self.__read_rx())

    #Refresh all solenoids from pixel data.
    def refresh(self):
        self.__port.write('REFRESH\n'.encode('utf-8'))
        print(self.__read_rx())

    #Stop all solenoids by turning them off.
    def stop(self):
        self.__port.write('STOP\n'.encode('utf-8'))
        print(self.__read_rx())

    #Set the state (0/1) for the specified solenoid index (0-79). Example: SETBIT 62 1
    def set_bit(self,EVI,state):
        self.__port.write('SETBIT {0} {1}\n'.format(EVI,state).encode('utf-8'))
        print(self.__read_rx())

    #Set the states (0-FF) for the specified byte index (0-9). Example: SETBYTE 3 F3
    def set_byte(self,byte,state):
        self.__port.write('SETBYTE {0} {1}\n'.format(byte,state).encode('utf-8'))
        print(self.__read_rx())

    #Set the state (0=Off, 1=On) for the specified status LED (1-3). Example: SETLED 2 1
    def set_led(self,Led,state):
        self.__port.write('SETLED {0} {1}\n'.format(Led,state).encode('utf-8'))
        print(self.__read_rx())

    #Display the states for the option switches
    def get_switches(self):
        self.__port.write('GETSWITCHES\n'.encode('utf-8'))
        print(self.__read_rx())

    #closes the serial port
    def close(self):
        self.__port.close()

    #reads in data on the serial line
    def __read_rx(self):
        self.__port.flush()
        return self.__port.read_until('').decode('utf-8')
