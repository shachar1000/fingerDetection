#include <Servo.h>
int buzzer = 2;
static const uint8_t analog_pins[] = {A0,A1,A2};
int r0s[] = {130, 10, 30};
int r90s[] = {30, 110, 120};
long REFRESH_INTERVALX = 300;
long lastRefreshTime = 0;
int last = 0;
Servo servos[3];
void setup() {
  Serial.begin(9600);
  for (int i = 3; i <= 7; i++) {
    pinMode(i, OUTPUT);
  }
  pinMode(buzzer, OUTPUT);
  for (int i = 0; i < 3; i++) {
    servos[i].attach(analog_pins[i]);
  }
}

void loop() {
  while (Serial.available()) {
    if(millis() - lastRefreshTime >= REFRESH_INTERVALX)
    {
      lastRefreshTime += REFRESH_INTERVALX;
      for (int i = 0; i < 3; i++) {
        if (last == 90) {
          servos[i].write(r90s[i]);
        } else {
          servos[i].write(r0s[i]);
          }
        }
      last = last == 90 ? 0 : 90;
    }
    if (incomingData == 'Y') {
      tone(buzzer, 1000);
      Serial.println("cool");
    }
    if (incomingData == 'N') {
      noTone(buzzer);
    }
  }
}
