
#ifndef Chip_Timing_library_h
#define Chip_Timing_library_h

#include "Arduino.h"


class FC_mechanics {


public:
  //initialize size of chip
  FC_mechanics(int rows, int columns,int ts[][], int th[][], int tpw[][]));

  //update state of the chip
  //checks if the latch and data line have been on long enough to change state
  //if valid input change state
  bool check_inputs();

  //get the state of the chip
  int[][] get_state();


private:
  //size of the chip
  int rows;
  int columns;


  //internal state of the chip
  int state [100][100];


  //benchmark data of the chip
  int ts[100][100];
  int th[100][100];
  int tpw[100][100];

  //arrays for latch and data pin locations
  int latchPins[100];
  int dataPins[100];

  //arrays for last time of pin rise/fall edge
  int latchPin_times[100][2];
  int dataPin_times[100][2];

  //arrays for last time of pin state change
  int latchPin_states[100][2];
  int dataPin_states[100][2];

  //state change calculator that takes the change times for both and their current state and the previous state and time
  int state_updater(int state, int minS, int minH, int minPW, int latchEdge1, int latchEdge2, int dataEdge1, int dataEdge2, int latchState1, int latchState2, int dataState1, int dataState2);

  };

  #endif
