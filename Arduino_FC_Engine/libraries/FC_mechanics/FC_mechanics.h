
#ifndef Chip_Timing_library_h
#define Chip_Timing_library_h

#include "Arduino.h"


class FC_mechanics {


public:
  //initialize size of chip
  FC_mechanics(int rows, int columns,int setup[][], int hold[][], int pw[][]));

  //update state of the chip
  //checks if the latch and data line have been on long enough to change state
  //if valid input change state
  bool check_inputs();

  //get the state of the chip
  int[][] get_state()


private:
  //size of the chip
  int rows;
  int columns;


  //internal state of the chip
  int state [100][100];


  //benchmark data of the chip
  int setup[100][100];
  int hold[100][100];
  int pw[100][100];

  //arrays for latch and data pin locations
  int latchPins[100];
  int dataPins[100];

  };

  #endif
