#include "Arduino.h"
#include "FC_mechanics.h"

//input the rows and columns of the chip and record the setup, hold, pw required to make a valid input
FC_mechanics::FC_mechanics(int rows, int columns,int setup[][], int hold[][], int pw[][])) {
  this->rows = rows;
  this->columns = columns;
  this->setup[0][0] = setup;
  this->hold[0][0] = hold;
  this->pw[0][0] = pw;

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

//


//give the current state of the device
FC_mechanics::get_state(){
  return this->state[rows][columns]
}

//Sets up a test with a specified setup time, hold time, and pulse width
//ts is setup time; tpw is the pulse width time; th is the hold time
//takes in microsecond delay
void cellTest::timing_trigger(signed long ts, signed long tpw, signed long th) {
  //boolean values to determine if each pulse has ran
  bool setup_ran = false;
  bool pulse_start = false;
  bool pulse_end = false;
  bool hold_ran = false;


  //determine trigger times relative to the negative edge of pulse
  unsigned long elapsed_time;
  unsigned long pw_trigger_time = 500000;
  unsigned long setup_trigger_time = pw_trigger_time - ts;
  unsigned long hold_trigger_time = pw_trigger_time + th;
  unsigned long pw_end_time = pw_trigger_time + tpw;

   // Serial.println(pw_trigger_time);
   // Serial.println(setup_trigger_time);
   // Serial.println(hold_trigger_time);
   // Serial.println(pw_end_time);

  digitalWrite(led, LOW);
  this->start_time = micros();

  //maybe change? start time after delay

  //delay on the front end
  delay(100);

  //wait for time to elapse and trigger elements on the proper times
  while (!(setup_ran && pulse_start && pulse_end && hold_ran)) {
    elapsed_time = micros() - start_time;


    //trigger setup change relative to pulse width trigger
    if ((elapsed_time >= setup_trigger_time) && !setup_ran) {
      trigger_setup(final_state1);
      setup_ran = true;
    }

    //trigger the pulse at the trigger time
    if ((elapsed_time >= pw_trigger_time) && !pulse_start) {
      trigger_pulse();
      pulse_start = true;
    }

    //trigger hold change after hold time
    if ((elapsed_time >= hold_trigger_time) && !hold_ran) {
      trigger_hold(final_state1);
      hold_ran = true;
    }

    //end pulse after pulse trigger time
    if ((elapsed_time >= pw_end_time) && !pulse_end) {
      end_pulse();
      pulse_end = true;
    }

  }

  //delay longer on the backend if the final state is 0
  if (final_state1) {
    delay(200);
  } else {
    delay(600);
  }

  //all triggers done
  digitalWrite(led, HIGH);

}

//Same as timing trigger but dual
//ts is setup time; tpw is the pulse width time; th is the hold time
//takes in microsecond delay
void cellTest::dual_timing_trigger(signed long ts, signed long tpw, signed long th){
  //boolean values to determine if each pulse has ran
  bool setup_ran = false;
  bool pulse_start = false;
  bool pulse_end = false;
  bool hold_ran = false;

  //determine trigger times relative to the negative edge of pulse
  unsigned long elapsed_time;
  unsigned long pw_trigger_time = 50;
  unsigned long setup_trigger_time = pw_trigger_time - ts;
  unsigned long hold_trigger_time = pw_trigger_time + th;
  unsigned long pw_end_time = pw_trigger_time + tpw;

  //  Serial.println(pw_trigger_time);
  //  Serial.println(setup_trigger_time);
  //  Serial.println(hold_trigger_time);
  //  Serial.println(pw_end_time);

  digitalWrite(led, LOW);
  this->start_time = micros();

  //maybe change? start time after delay

  //delay on the front end
  //delay(100);

  //wait for time to elapse and trigger elements on the proper times
  while (!(setup_ran && pulse_start && pulse_end && hold_ran)) {
    elapsed_time = micros() - start_time;


    //trigger setup change relative to pulse width trigger
    if ((elapsed_time >= setup_trigger_time) && !setup_ran) {
      trigger_setup(final_state1);
      test_col++;
      trigger_setup(final_state2);
      test_col--;
      //add one to column and start
      setup_ran = true;
      Serial.print("time elapsed for data line start "); Serial.print(elapsed_time / 1000);
      Serial.print(" milliseconds");
      Serial.println();
    }

    //trigger the pulse at the trigger time
    if ((elapsed_time >= pw_trigger_time) && !pulse_start) {
      trigger_pulse();
      test_col++;
      trigger_pulse();
      test_col--;
      pulse_start = true;
      Serial.print("time elapsed for gate line start "); Serial.print(elapsed_time / 1000);
      Serial.print(" milliseconds");
      Serial.println();
    }

    //trigger hold change after hold time
    if ((elapsed_time >= hold_trigger_time) && !hold_ran) {
      trigger_hold(final_state1);
      test_col++;
      trigger_hold(final_state2);
      test_col--;
      hold_ran = true;
      Serial.print("time elapsed for data line end "); Serial.print(elapsed_time / 1000);
      Serial.print(" milliseconds");
      Serial.println();
    }

    //end pulse after pulse trigger time
    if ((elapsed_time >= pw_end_time) && !pulse_end) {
      end_pulse();
      test_col++;
      end_pulse();
      test_col--;
      pulse_end = true;
      Serial.print("time elapsed for gate line end "); Serial.print(elapsed_time / 1000);
      Serial.print(" milliseconds");
      Serial.println();
    }

  }

  //delay longer on the backend if the final state is 0
  // if (final_state) {
  //   delay(200);
  // } else {
  //   delay(600);
  // }

  //all triggers done
  digitalWrite(led, HIGH);
}
