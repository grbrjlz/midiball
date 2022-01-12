#include <Controlino.h>
#include <Midier.h>

//midier::Layers<8> layers;
//midier::Sequencer sequencer(layers);
const int buttonPin = 2;     // the number of the pushbutton pin
// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
boolean isPressed = false;

void setup() {
  // initialize the LED pin as an output:
  //pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
}


void loop() {
  // read the state of the pushbutton value:
  
  buttonState = digitalRead(buttonPin);
  //Serial.println(buttonState);
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    isPressed = true;   
    // turn LED on:
    //digitalWrite(ledPin, HIGH);
  } else {
    if (isPressed == true) {
      Serial.print(0);
    }
    isPressed = false;
  }
}
