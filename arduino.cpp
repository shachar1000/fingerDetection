#include <Servo.h>

byte incomingData;
int buzzer = 2;

static const uint8_t analog_pins[] = {A0,A1,A2};


Servo servos[5];

void setup() {
  Serial.begin(9600);
  for (int i = 3; i <= 7; i++) {
    pinMode(i, OUTPUT);
  }
  pinMode(buzzer, OUTPUT);

  for (int i=0; i<3; i++) {
    servos[i].attach(analog_pins[i]);
  }

}

void loop() {


  for (int i=0; i < 3; i++) {
        servos[i].write(0);
      }
   while (Serial.available()) {
    incomingData = Serial.read();
    for (int j = 3; j <= 7; j++) {
      digitalWrite(j, LOW);
    }
    if (incomingData == 'Y') {
      tone(buzzer, 1000);
      Serial.println("cool");
    }
    if (incomingData == 'N') {
      noTone(buzzer);
    }

    if (incomingData == '1') {
    int i = 2;
      for (int j = 1; j <= i; j++) {
        digitalWrite(2+j, HIGH);
      }
      for (int i=0; i < 1; i++) {
        servos[i].write(180);
      }
    }
    if (incomingData == '2') {
    int i = 3;
      for (int j = 1; j <= i; j++) {
        digitalWrite(2+j, HIGH);
      }
      for (int i=0; i < 2; i++) {
        servos[i].write(180);
      }
    }
    if (incomingData == '3') {
    int i = 4;
      for (int j = 1; j <= i; j++) {
        digitalWrite(2+j, HIGH);
      }
      for (int i=0; i < 3; i++) {
        servos[i].write(180);
      }
    }
    if (incomingData == '4') {
    int i = 5;
      for (int j = 1; j <= i; j++) {
        digitalWrite(2+j, HIGH);
      }
    }
    if (incomingData == '5') {
    int i = 5;
      for (int j = 1; j <= i; j++) {
        digitalWrite(2+j, HIGH);
      }
    }



//    for (int i = 0; i <= 5; i++) {
//      if (incomingData == String(i)) {
//        for (int j = 1; j <= i; j++) {
//          digitalWrite(2+j, HIGH);
//        }
//      }
//    }
          Serial.println(incomingData);
//        for (int j = 1; j <= i; j++) {
//          digitalWrite(2+j, HIGH);
//        }


   }
}
