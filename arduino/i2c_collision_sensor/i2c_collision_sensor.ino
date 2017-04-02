// I2C Collision Sensor
// by Luc Desrosiers

// Monitor the infrared sensors (Left and Right sensors)
// Transfer sensor state whenever the master asks

// Created February 2107

#include <Wire.h>

#define SLAVE_ADDRESS 0x04

#define IR_SENSOR_PIN 4
#define IR_LEFT_LED_PIN 2
#define IR_RIGHT_LED_PIN 3

#define HC_TRIGGER_PIN 6
#define HC_ECHO_PIN 5

#define POWER_PIN 7

// Global Variables
int currentIRPin = IR_LEFT_LED_PIN;
int distance = 0;
int leftCollision = 0;
int rightCollision = 0;
uint8_t xmitBuffer[2];

void setup() {
  //Serial Console setup
  Serial.begin(9600);  
  
  // i2c Setup
  Wire.begin(SLAVE_ADDRESS);               
  Wire.onRequest(i2cTransmit); 

  // Power Pin Setup
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, HIGH);
             
  // Infrared Setup
  pinMode(IR_LEFT_LED_PIN, OUTPUT);
  digitalWrite(IR_LEFT_LED_PIN, LOW);
  pinMode(IR_RIGHT_LED_PIN, OUTPUT);
  digitalWrite(IR_RIGHT_LED_PIN, LOW);

  // Ultrasound Setup
  pinMode(HC_TRIGGER_PIN, OUTPUT);
  digitalWrite(HC_TRIGGER_PIN, LOW);
  pinMode(HC_ECHO_PIN, INPUT);

  fillBuffer();
}

void loop() {
  leftCollision = checkForCollision(IR_LEFT_LED_PIN);
  delay(50);
  rightCollision = checkForCollision(IR_RIGHT_LED_PIN);
  distance = measureDistance();
  fillBuffer();
  delay(50);
}

int checkForCollision(int ledId) {
  irLedWrite(ledId);
  int result = (digitalRead(IR_SENSOR_PIN) == LOW);

  return result;
}

void irLedWrite(int ledId) {
  for (int i = 0; i <= 384; i++) {
    digitalWrite(ledId, HIGH);
    delayMicroseconds(13);
    digitalWrite(ledId, LOW);
    delayMicroseconds(13);
  }
}

void fillBuffer() {
  xmitBuffer[0] = leftCollision | (rightCollision << 1);
  xmitBuffer[1] = distance;
  Serial.println("Left:");
  Serial.println(leftCollision);
  Serial.println("Right:");
  Serial.println(rightCollision);
  Serial.println("Buffer:");
  Serial.println(xmitBuffer[0]);
  Serial.println("Distance:");
  Serial.println(xmitBuffer[1]);
}

void i2cTransmit() {
  Wire.write(xmitBuffer,2);
}

int measureDistance() {
  long duration;
  digitalWrite(HC_TRIGGER_PIN, LOW);  
  delayMicroseconds(2); 
  digitalWrite(HC_TRIGGER_PIN, HIGH);
  
  delayMicroseconds(10);
  digitalWrite(HC_TRIGGER_PIN, LOW);
  duration = pulseIn(HC_ECHO_PIN, HIGH);
  int dist = (duration / 2) / 29.1;
  
  if (dist >= 200 || dist <= 0) {
    return 0;
  }
  else {
    return dist;
  }
}


