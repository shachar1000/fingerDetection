#include <Servo.h>
//nigga
long REFRESH_INTERVALX = 100;
long lastRefreshTime = 0;
static const uint8_t analog_pins[] = {A0,A1,A2};
Servo servos[3];

void setup() {
  Serial.begin(9600);
  for (int i = 3; i <= 7; i++) {
    pinMode(i, OUTPUT);
  }
//  pinMode(buzzer, OUTPUT);
  for (int i = 0; i < 3; i++) {
    servos[i].attach(analog_pins[i]);
  }
  Serial.setTimeout(10);
}

void loop() {
//  if(millis() - lastRefreshTime >= REFRESH_INTERVALX) {
//    lastRefreshTime += REFRESH_INTERVALX;
    String incoming = Serial.readString();
    for (int i = 0; i < 5; i++) {
//      Serial.println(String(i));
//      Serial.println(Serial.readString());
      if (incoming[1] == String(i)[0]) { // i = number of fingers
        if (i == 0) {
          for (int d = 0; d < 3; d++) {
              servos[d].write(0);
          }
        }
        for (int j = 1; j < i+2; j++) { // j = index of fingers
          // for each finger
          digitalWrite(2+j, HIGH);
          if (j < 4 && i != 0) {
            servos[j-1].write(90);
          } if (j == i) {
            for (int d = 2; d > j; d--) {
              servos[d].write(0);
            }
          }
        }
         int turnOffLed = (5-i-1);
         for (int m = 0; m < turnOffLed; m++) {
           digitalWrite(7-m, LOW);
         }
      }
    }
  //}
}



