#include <Servo.h>   // Library to control servo motors

// Ultrasonic sensor pin definitions
#define trigPin 10   // Trigger pin sends ultrasonic pulse
#define echoPin 11   // Echo pin receives reflected pulse

Servo myServo;       // Create servo object

long duration;       // Time taken for ultrasonic pulse to return
int distance;        // Calculated distance in centimeters

void setup() {
  // Attach servo to digital pin 9
  myServo.attach(9);

  // Move servo to center position (90 degrees)
  myServo.write(90);
  delay(1000);       // Give servo time to reach position

  // Configure ultrasonic sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Start serial communication for debugging/data output
  Serial.begin(9600);
}

/*
  Function: getDistance()
  Purpose : Measures distance using ultrasonic sensor
  Returns :
    - Distance in centimeters (valid range 5–50 cm)
    - -1 if no echo or out-of-range reading
*/
int getDistance() {

  // Ensure trigger pin is LOW before sending pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Send 10 microsecond HIGH pulse to trigger ultrasonic burst
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure duration of echo pulse (timeout = 30 ms)
  duration = pulseIn(echoPin, HIGH, 30000);

  // If no echo received, return invalid reading
  if (duration == 0) return -1;

  // Convert time to distance (speed of sound = 0.034 cm/µs)
  int d = duration * 0.034 / 2;

  // Ignore distances outside desired range
  if (d < 5 || d > 50) return -1;

  return d;  // Return valid distance
}

void loop() {

  // Sweep servo from 0° to 180°
  for (int pos = 0; pos <= 180; pos++) {
    myServo.write(pos);   // Move servo to current angle
    delay(25);            // Allow servo to settle

    distance = getDistance();  // Measure distance

    // Output angle and distance in CSV format
    Serial.print(pos);
    Serial.print(",");

    // Print "-" if distance is invalid
    if (distance == -1) {
      Serial.println("-");
    } else {
      Serial.println(distance);
    }
  }

  // Sweep servo from 180° back to 0°
  for (int pos = 180; pos >= 0; pos--) {
    myServo.write(pos);
    delay(25);

    distance = getDistance();

    Serial.print(pos);
    Serial.print(",");

    if (distance == -1) {
      Serial.println("-");
    } else {
      Serial.println(distance);
    }
  }
}
