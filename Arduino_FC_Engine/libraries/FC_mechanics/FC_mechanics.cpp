#include "Arduino.h"
#include "FC_mechanics.h"

//input the rows and columns of the chip and record the ts, th, pw required to make a valid input
FC_mechanics::FC_mechanics(int rows, int columns,int ts[20][20], int th[20][20], int tpw[20][20]) {
  this->rows = rows;
  this->columns = columns;
  for(int i = 0; i < rows; i++){
    for(int j = 0; j < columns; j++){
      this->ts[i][j] = ts[i][j];
      this->th[i][j] = th[i][j];
      this->tpw[i][j] = tpw[i][j];
    }
  }

  //initialize data and latch lines
  //initialize latch lines as even numbers 22 to 52
  for (int latchPin = 0; latchPin/2 < rows && (latchPin + 22 <= 52); latchPin += 2) {
    latchPins[latchPin/2] = latchPin + 22;
    pinMode(latchPins[latchPin], INPUT);
  }

  //initialize data lines as odd numbers 23 to 53
  for (int dataPin = 0; dataPin/2 < columns && (dataPin + 23 <= 53); dataPin += 2) {
    dataPins[dataPin/2] = dataPin + 23;
    pinMode(dataPins[dataPin], INPUT);
  }

}

//update how long the latch and data pins have been open
bool FC_mechanics::check_inputs() {
  //latch and data dummy variables to compare previous states
  int L = 0;
  int D = 0;

  //int elapsed_time;

  //get the latch and data pin states
  for(int i = 0; i < rows; i++) {
    //elapsed_time = micros();
    L = digitalRead(latchPins[i]);
    //Serial.print("time to digitalRead latch "); Serial.println(micros() - elapsed_time);
    if (latchPin_state[i] != L) {
      Serial.print(latchPin_state[i]); Serial.print("->"); Serial.print(L); Serial.print("latchPin"); Serial.println(latchPins[i]);
      //Serial.print("at "); Serial.println(millis());
      //if the previous state is not the same state push the state change
      latchPin_time[i] = millis();
    }
    latchPin_state[i] = L;
  }
  for(int i = 0; i < columns; i++) {
    //elapsed_time = micros();
    D = digitalRead(dataPins[i]);
    //Serial.print("time to digitalRead latch "); Serial.println(micros() - elapsed_time);
    if (dataPin_state[i] != D) {
      Serial.print(dataPin_state[i]); Serial.print("->"); Serial.print(D); Serial.print("dataPin"); Serial.println(dataPins[i]);
      //Serial.print("at "); Serial.println(millis());
      //if the previous state is not the same state record the time of change
      dataPin_time[i] = millis();
    }
    dataPin_state[i] = D;
  }

  int new_state;
  bool state_change = false;
  //get the state changes based on the the data and latch change times
  for(int row = 0; row < rows; row++){
    for(int column = 0; column < columns; column++){

      new_state = state_updater(state[row][column],ts[row][column],th[row][column],tpw[row][column],dataPin_time[column],latchPin_time[row],dataPin_state[column],latchPin_state[row]);
      //if the new state is different signal a state change
      if (new_state != state[row][column]){
        state[row][column] = new_state;
        state_change = true;
      }

    }
  }

  return state_change;

}


//state updater
int FC_mechanics::state_updater(int currentState, int minS, int minH, int minPW, int dataEdge, int latchEdge, int dataState, int latchState){
  //Serial.print("state "); Serial.print(state); Serial.print("| latchEdge1 "); Serial.print(latchEdge1); Serial.print("| latchEdge2 "); Serial.print(latchEdge2); Serial.print("| dataEdge1 "); Serial.print(dataEdge1); Serial.print("| dataEdge2 "); Serial.print(dataEdge2); Serial.print("| latchState1 "); Serial.print(latchState1); Serial.print("| latchState2 "); Serial.print(latchState2); Serial.print("| dataState1 "); Serial.print(dataState1); Serial.print("| dataState2 "); Serial.println(dataState2);
  int latchSteady_time = millis() - latchEdge;
  int dataSteady_time = millis() - dataEdge;
    //calculate the current setup, hold, and pw
    int s = latchEdge - dataEdge;
    int h;
    if (dataEdge > latchEdge){
      h = dataSteady_time - s;
    } else {
      h = millis() - latchEdge;
    }
    int pw = latchSteady_time;

    if (latchState == 0){
      Serial.print("state "); Serial.print(currentState); Serial.print("| latchEdge "); Serial.print(latchEdge); Serial.print("| dataEdge "); Serial.print(dataEdge); Serial.print("| dataState "); Serial.print(dataState); Serial.print("| latchState "); Serial.println(latchState);
      Serial.print("latchSteady_time "); Serial.print(latchSteady_time); Serial.print("| dataSteady_time "); Serial.print(dataSteady_time); Serial.print("| s "); Serial.print(s); Serial.print("| h "); Serial.print(h); Serial.print("| pw "); Serial.println(pw);
    }

    //make sure that the setup, hold, and pulse width fit within the physical contraints of the FC
    if(s > minS && h > minH && pw > minPW && latchState == 0){
      //if the physical constraints fit then change state
      return dataState;
    } else {
      return currentState;
    }

}



//give the current state of the device
int FC_mechanics::get_state(int row, int column){
  return state[row][column];
}
