
#ifndef Chip_Timing_library_h
#define Chip_Timing_library_h

#include "Arduino.h"


class FC_mechanics {


public:
  //initialize size of chip
  FC_mechanics(int rows, int columns,int ts[20][20], int th[20][20], int tpw[20][20]);

  //update state of the chip
  //checks if the latch and data line have been on long enough to change state
  //if valid input change state
  bool check_inputs(void);

  //get index of the state of the chip
  int get_state(int row, int column);


private:
  //size of the chip
  int rows;
  int columns;


  //internal state of the chip
  int state [20][20];


  //benchmark data of the chip
  int ts[20][20];
  int th[20][20];
  int tpw[20][20];

  //arrays for latch and data pin locations
  int latchPins[20];
  int dataPins[20];

  //arrays for last time of pin rise/fall edge
  int latchPin_time[20];
  int dataPin_time[20];

  //arrays for last time of pin state change
  int latchPin_state[20];
  int dataPin_state[20];

  //takes in the time that latch has been open if it is open and the last edge of data
  int state_updater(int currentState, int minS, int minH, int minPW, int dataEdge, int latchEdge, int dataState, int latchState);

  };

  #endif
