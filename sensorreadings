void setup() {
  Serial.begin(9600); // Initialize UART communication
}

void loop() {
  // Read sensor values
  int sensor1 = analogRead(A0);
  int sensor2 = analogRead(A1);
  int sensor3 = analogRead(A2);
  int sensor4 = analogRead(A3);
  int sensor5 = analogRead(A4);
  int sensor6 = analogRead(A5);
  int sensor7 = analogRead(A6);
  int sensor8 = analogRead(A7);

  // Send sensor data via UART
  Serial.print(sensor1);
  Serial.print(",");
  Serial.print(sensor2);
  Serial.print(",");
  Serial.print(sensor3);
  Serial.print(",");
  Serial.print(sensor4);
  Serial.print(",");
  Serial.print(sensor5);
  Serial.print(",");
  Serial.print(sensor6);
  Serial.print(",");
  Serial.print(sensor7);
  Serial.print(",");
  Serial.println(sensor8); // Use println for the last value to send newline

  delay(1000); // Wait for 1 second before the next read
}
