**Code Overview**



1\. Servo Sweep Code (Arduino)

* Controls the servo motor.
* Sweeps the servo from 0° to 180° and back to 0° continuously.
* Used to rotate the ultrasonic sensor for scanning.



2\. Ultrasonic Sensor Code (Arduino)

* Reads distance data from the ultrasonic sensor.
* Calculates and outputs the distance based on echo time.
* Used independently to test sensor functionality.



3\. Sonar Code (Arduino)

* Combines servo movement and ultrasonic sensing.
* Outputs angle and distance values in real time via the serial monitor.
* This is the main Arduino sketch used for the full system.



4\. Sonar Visualization Code (Python)

* Reads angle and distance data from the Arduino via the serial port.
* Displays a sonar-style UI.
* A sweeping line represents the servo angle.
* Red dots represent detected objects.



**Instructions**



Before uploading any Arduino sketch:

* Select the correct Arduino board and COM port in the Arduino IDE.



Before running the Python program:

* Update the COM port in the Python script to match the Arduino’s serial port.
* Ensure the required Python libraries are installed.



