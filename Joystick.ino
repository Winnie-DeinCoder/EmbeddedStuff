const int joyXpin = A0;
const int joyYpin = A1;
const int switchPin = 2;


void setup() {
  Serial.begin(9600);
  pinMode(switchPin,INPUT_PULLUP)

}

void loop() {
  int joyX = analogRead(joyXpin);
  int joyY = analogRead(joyYpin);
  int switchState = digitalRead(switchPin);

  Serial.print(joyX);
  Serial.print(",");
  Serial.print(joyY);
  Serial.print(",");
  Serial.print(switchState);
  delay(100);


}
