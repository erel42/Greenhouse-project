#define REDPIN 3
#define GREENPIN 5
#define BLUEPIN 6

void setup() {
  // put your setup code here, to run once:
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);

  digitalWrite(REDPIN, HIGH);
  digitalWrite(GREENPIN, HIGH);
  digitalWrite(BLUEPIN, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:

}
