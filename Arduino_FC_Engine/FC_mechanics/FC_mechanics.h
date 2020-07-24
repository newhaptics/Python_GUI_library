
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
  int state [][];


  //benchmark data of the chip
  int setup[][];
  int hold[][];
  int pw[][];

  };

  #endif
