**Wiring Diagram Explanation**



**Main components:**

* Arduino Nano
* Ultrasonic Sensor (HC-SR04 or similar)
* Servo Motor (SG40)
* Capacitor (for power stabilization)
* Breadboard
* Jumper Wires



**Connections:**



Arduino Nano Power:

* 5V → Servo VCC
* 5V → Ultrasonic Sensor VCC
* GND → Servo GND
* GND → Ultrasonic Sensor GND



Servo Motor:

* Red wire (VCC) → 5V
* Brown/Black wire (GND) → GND
* Orange/White wire (Signal) → Digital Pin 9



Ultrasonic Sensor:

* VCC → 5V
* GND → GND
* TRIG → Digital Pin 10
* ECHO → Digital Pin 11



Capacitor:

* Connected across 5V and GND
* Used to smooth voltage and prevent servo noise or resets
* Observe polarity if using an electrolytic capacitor



**Notes**

* Make sure all grounds are common.
* The capacitor is recommended, especially if the servo draws high current.
* Use a stable power source to avoid brownouts.



**Optional**



For a more robust and clean build, custom 3D printed parts can be used:

* Servo Casing
* Ultrasonic Sensor Casing
* Servo Arm Mount
* Breadboard Mount



These parts help with proper alignment, durability, and overall mounting stability.



3D printable files are available via my Printables profile: https://www.printables.com/model/1550105-sonar-style-distance-sensing-system-parts
