#include "Arduino.h"
#include "FC_mechanics.h"

//input the rows and columns of the chip and record the ts, th, pw required to make a valid input
FC_mechanics::FC_mechanics(int rows, int columns,int ts[][], int th[][], int tpw[][])) {
  this->rows = rows;
  this->columns = columns;
  this->ts[0][0] = ts;
  this->th[0][0] = th;
  this->tpw[0][0] = tpw;

  //initialize data and latch lines
  //initialize latch lines as even numbers 22 to 52
  for (int latchPin = 0; latchPin < rows && (latchPin + 22 =< 52); latchPin += 2) {
    latchPins[latchPin] = latchPin + 22;
    pinMode(latchPins[latchPin], INPUT);
  }

  //initialize data lines as odd numbers 23 to 53
  for (int dataPin = 0; dataPin < columns && (dataPin + 23 =< 53); dataPin += 2) {
    dataPins[dataPin] = dataPin + 23;
    pinMode(dataPins[dataPin], INPUT);
  }

}

//update how long the latch and data pins have been open
bool FC_mechanics::check_inputs() {
  //latch and data dummy variables to compare previous states
  int L = 0;
  int D = 0;

  //get the latch and data pin states
  for(int i = 0; i < rows; i++) {
    L = digitalRead(latchPins[i]);
    if (latchPin_states[i][0] != L) {
      //if the previous state is not the same state push the state change
      latchPin_times[i][1] = latchPin_times[i][0];
      latchPin_times[i][0] = millis();
      latchPin_states[i][1] = latchPin_states[i][0];
      latchPin_states[i][0] = L;
    }
  }
  for(int i = 0; i < columns; i++) {
    D = digitalRead(dataPins[i]);
    if (dataPin_states[i] != D) {
      //if the previous state is not the same state record the time of change
      dataPin_times[i][1] = dataPin_times[i][0];
      dataPin_times[i][0] = millis();
      dataPin_states[i][1] = dataPin_states[i][0];
      dataPin_states[i][0] = D;
    }
  }

  int new_state;
  bool state_change = false;
  //get the state changes based on the the data and latch change times
  for(int row = 0; i < rows; row++){
    for(int column = 0; i < columns; column++){

      new_state = state_updater(state[row][column], ts[row][column], th[row][column], tpw[row][column], latchPin_times[row][0],latchPin_times[row][1],dataPin_times[column][0],dataPin_times[column][1],dataPin_states[column][0],dataPin_states[column][1],latchPin_states[row][0],latchPin_states[row][1]);
      //if the new state is different signal a state change
      if (new_state != state[row][column]){
        state[row][column] = new_state;
        state_change = true;
      }

    }
  }
  
  return state_change

}


//state updater
int FC_mechanics::state_updater(int state ,int minS, int minH, int minPW, int latchEdge1, int latchEdge2, int dataEdge1, int dataEdge2, int latchState1, int latchState2, int dataState1, int dataState2){


  //first deteremine if latch went low or HIGH
  if (latchState1 > latchState2) {
    //calculate the current setup, hold, and pw
    int s = latchEdge1 - dataEdge1;
    int h = dataEdge2 - latchEdge1;
    int pw = latchEdge2 - latchEdge1;

    //make sure that the setup, hold, and pulse width fit within the physical contraints of the FC
    if(s > minS && h > minH && pw > minPW){
      //if the physical constraints fit then change state
      return dataState2
    } else {
      return state
    }

  } else {
    return state
  }

}



}

//give the current state of the device
int[][] FC_mechanics::get_state(){
  return this->state[rows][columns]
}
