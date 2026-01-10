#define trigPin 10
#define echoPin 11

long duration;
int distance;

void setup() {
  // put your setup code here, to run once:

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:  

  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Send 10µs pulse to trigger pin
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo pin
  duration = pulseIn(echoPin, HIGH, 30000); // timeout ~5m

  // If no echo received
  if (duration == 0) {
    Serial.println("-");
  } else {
    // Calculate distance (cm)
    distance = duration * 0.034 / 2;

    // Check range: 5 cm to 200 cm
    if (distance >= 5 && distance <= 200) {
      Serial.print("Distance: ");
      Serial.print(distance);
      Serial.println(" cm");
    } else {
      Serial.println("-");
    }
  }

  delay(500);
}
