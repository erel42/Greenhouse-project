int i;
String input;
bool exit_switch;

void LEDon();
void LEDoff();

void setup()
 
{

pinMode(13, OUTPUT);

Serial.begin(9600);

while (!Serial);

Serial.println("Input 1 to Turn LED on and 2 to off");

}

void loop() {
  if (Serial.available())
  {
    input = Serial.readString();
    i = 0;
    Serial.println(input);
    exit_switch = false;
    while(!exit_switch && i < input.length())
    {
      switch(input[i])
      {
        case ('1'): //LED on
          LEDon();
          exit_switch = true;
          break;
        case ('2'): //LED off
          LEDoff();
          exit_switch = true;
          break;
      }
      i++;
    }
  }
}

void LEDon()
{
  digitalWrite(13, HIGH);
  
  Serial.println("Command completed LED turned ON");
}

void LEDoff()
{
  digitalWrite(13, LOW);

  Serial.println("Command completed LED turned OFF");
}
