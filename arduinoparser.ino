int sensorValue = 0;  // value read from the pot
int outputValue = 0;  // value output to the PWM (analog out)
int PWMValue = 0;
int nsample = 100; //number of samples to average
int ledPins[] = {2, 3, 4, 5, 6, 7, 8}; // an array of pin numbers to which LEDs are attached
int pinCount = 8;  // the number of pins (i.e. the length of the array)
int ADCchans[] = {A0, A1, A2, A3, A4, A5, A6, A7};  //ADC channels, sorted to match PWM pins
int ADCvals[] = {-1, -1, -1, -1, -1, -1, -1, -1};
void setup() {
  // Initialize each pin as an output:
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    pinMode(ledPins[thisPin], OUTPUT);
  }
  // Initialize serial communications at 9600 bps:
  Serial.begin(9600);
}
void readADCs() {
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    unsigned int accum = 0;
    unsigned int n = 0;
    while (n < nsample) {
      accum += analogRead(ADCchans[thisPin]);
      n += 1;
    }
    ADCvals[thisPin] = accum / nsample;
  }
}
void sendSensorData(int sensorID, int sensorValue) {
  int packetLength = 4 + sizeof(sensorValue); // Packet length: 1 byte for ID, 1 byte for length, 2 bytes for value, 1 byte for checksum
  int checksum = (sensorID + packetLength + (sensorValue & 0xFF) + ((sensorValue >> 8) & 0xFF));

    byte sensorIDBytes[sizeof(int)];
    byte packetLengthBytes[sizeof(int)];
    byte sensorValueBytes[sizeof(int)];
    byte checkSumBytes[sizeof(int)];

    memcpy(sensorIDBytes, &sensorID, sizeof(int));
    memcpy(packetLengthBytes, &packetLength, sizeof(int));
    memcpy(sensorValueBytes, &sensorValue, sizeof(int));
    memcpy(checkSumBytes, &checksum, sizeof(int));

    Serial.print(checksum);
 
    Serial.write('<');  // Start marker
    Serial.write(sensorIDBytes, sizeof(int));
    Serial.write(',');
    Serial.write(packetLengthBytes, sizeof(int));
    Serial.write(',');
    Serial.write(sensorValueBytes, sizeof(int));
    Serial.write(',');
    Serial.write(checkSumBytes, sizeof(int));
    Serial.write('>'); 
 
  
}
void loop() {
  readADCs();
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    sendSensorData(thisPin, ADCvals[thisPin]); // Send sensor data
    PWMValue = map(ADCvals[thisPin], 0, 1023, 0, 255); // Scale value for PWM
    analogWrite(ledPins[thisPin], PWMValue); // Write to PWM pin for LED indication
  }
  delay(1000); // Wait for 500 milliseconds before the next loop
}
