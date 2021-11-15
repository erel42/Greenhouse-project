int state, i;
String input;
bool exit_switch;

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
  state = 0;
  i = 0;
  Serial.println(input);
  exit_switch = false;
  while(!exit_switch && i < input.length())
  {
    switch(input[i])
    {
      case ('1'): //LED on
        state = 1;
        exit_switch = true;
        break;
      case ('2'): //LED off
        state = 2;
        exit_switch = true;
        break;
    }
    i++;
  }

  if (state == 1)

  {

  digitalWrite(13, HIGH);

  Serial.println("Command completed LED turned ON");

  }

  if (state == 2)

  {

  digitalWrite(13, LOW);

  Serial.println("Command completed LED turned OFF");

  }
}
}
