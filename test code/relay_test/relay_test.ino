#define RELAY1_PIN 4
#define RELAY2_PIN 8
#define TAP_CLOSED_POSITION LOW

void setup() {
  // put your setup code here, to run once:
  digitalWrite(RELAY1_PIN, TAP_CLOSED_POSITION);
  digitalWrite(RELAY2_PIN, TAP_CLOSED_POSITION);
}

void loop() {
  digitalWrite(RELAY1_PIN, !TAP_CLOSED_POSITION);
  digitalWrite(RELAY2_PIN, TAP_CLOSED_POSITION);
  delay(1000);
  digitalWrite(RELAY1_PIN, TAP_CLOSED_POSITION);
  digitalWrite(RELAY2_PIN, !TAP_CLOSED_POSITION);
  delay(1000);
}
