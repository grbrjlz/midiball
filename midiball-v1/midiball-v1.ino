#include <Wire.h>
#include <Controlino.h>

const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.
int16_t accelerometer_x, accelerometer_y, accelerometer_z; // variables for accelerometer raw data
int16_t gyro_x, gyro_y, gyro_z; // variables for gyro raw data
// int16_t temperature; // variables for temperature data

const int FLEX_PIN = A0; // Pin connected to voltage divider output
// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float VCC = 4.98; // Measured voltage of Ardunio 5V line
const float R_DIV = 47500.0; // Measured resistance of 3.3k resistor

// accurately calculate bend degree.
const float STRAIGHT_RESISTANCE = 37300.0; // resistance when straight
const float BEND_RESISTANCE = 90000.0; // resistance at 90 deg

const int button1 = 2;     // the number of the pushbutton pin
const int button2 = 3;     // the number of the pushbutton pin
const int button3 = 4;     // the number of the pushbutton pin
// variables will change:
int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;// variable for reading the pushbutton status
boolean isPressed1 = false;
boolean isPressed2 = false;
boolean isPressed3 = false;


void setup() {
  // initialize the LED pin as an output:
  //pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  // initialize the pushbutton pin as an input:
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
  pinMode(FLEX_PIN, INPUT);
  
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR); // Begins a transmission to the I2C slave (GY-521 board)
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  
}


void loop() {

  // BUTTONS
  
  // Button 1 
  // read the state of the pushbutton value:
  buttonState1 = digitalRead(button1);
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState1 == HIGH) {
    isPressed1 = true;   
    // turn LED on:
    //digitalWrite(ledPin, HIGH);
  } else {
    if (isPressed1 == true) {
      int sig = 0;
      int number = -10;
      Serial.println(sig);
      Serial.println(number);
    }
    isPressed1 = false;
  }
  
  // Button 2 
  // read the state of the pushbutton value:
  buttonState2 = digitalRead(button2);
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState2 == HIGH) {
    isPressed2 = true;   
    // turn LED on:
    //digitalWrite(ledPin, HIGH);
  } else {
    if (isPressed2 == true) {
      int sig = 1;
      int number = -10;
      Serial.println(sig);
      Serial.println(number);
    }
    isPressed2 = false;
  }
  
  // Button 3 
  // read the state of the pushbutton value:
  buttonState3 = digitalRead(button3);
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState3 == HIGH) {
    isPressed3 = true;   
    // turn LED on:
    //digitalWrite(ledPin, HIGH);
  } else {
    if (isPressed3 == true) {
      int sig = 2;
      int number = -10;
      Serial.println(sig);
      Serial.println(number);
    }
    isPressed3 = false;
  }


  // GYRO 
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
  Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
  Wire.requestFrom(MPU_ADDR, 7*2, true); // request a total of 7*2=14 registers
  // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
  accelerometer_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  //temperature = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)
  gyro_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
  gyro_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  gyro_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)


  // BEND
  // Read the ADC, and calculate voltage and resistance from it
  
  int flexADC = analogRead(FLEX_PIN);
  float flexV = flexADC * VCC / 1023.0;
  float flexR = R_DIV * (VCC / flexV - 1.0);
  //Serial.println("Resistance: " + String(flexR) + " ohms");
  // Use the calculated resistance to estimate the sensor's
  // bend angle:
  float angle = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE, 0, 90.0);

  
  // SEND SIGNAL
  
  int sig = 3;
  Serial.println(sig); 
  Serial.println(accelerometer_y);
  
  
  sig = 4;
  Serial.println(sig); 
  Serial.println(accelerometer_z);
  
 
  int bend = angle;                
  sig = 5;
  Serial.println(sig); 
  Serial.println(bend);
  

  // delay
  delay(100);
  
}
