#include <Servo.h>

Servo myServo;

void setup() {
  // put your setup code here, to run once:

  myServo.attach(9);
  myServo.write(90);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Move from 0 to 180
  for (int pos = 0; pos <= 180; pos++) {
    myServo.write(pos);
    delay(25);
    Serial.println(pos);
  }

  // Move from 180 to 0
  for (int pos = 180; pos >= 0; pos--) {
    myServo.write(pos);
    delay(25);
    Serial.println(pos);
  }
}
