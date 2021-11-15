#define NUM_OF_VALUES 1
int i;
String input, data;
bool requestNewRecord = false;

double valueArr[NUM_OF_VALUES];

void LEDon();
void LEDoff();
void checkInput();
void updateValues();
void sendValues();

void setup()
{

pinMode(13, OUTPUT);

Serial.begin(9600);

while (!Serial);

Serial.println("Input 1 to Turn LED on and 2 to off");

}

void loop() {
  checkInput();
  updateValues();
  if (requestNewRecord)
    sendValues();
}

void updateValues()
{
  
}

void sendValues()
{
  data = "";
  data += valueArr[0];
  for(i = 1; i < NUM_OF_VALUES; i++)
  {
    data += ", ";
    data += valueArr[i];
  }
  Serial.println(data);
}

void checkInput()
{ //Needs rework
  if (Serial.available())
  {
    input = Serial.readString();
    i = 0;
    Serial.println(input);
    while(i < input.length())
    {
      if(input[i] > '0' && input[i] < 'z')
      {
        switch(input[i])
        {
          case ('1'): //LED on
            LEDon();
            break;
          case ('2'): //LED off
            LEDoff();
            break;
          case('r'):
            requestNewRecord = true;
            break;
        }
      }
      i++;
    }
  }
}

void LEDon()
{
  digitalWrite(13, HIGH);
  
  //Serial.println("Command completed LED turned ON");
}

void LEDoff()
{
  digitalWrite(13, LOW);

  //Serial.println("Command completed LED turned OFF");
}
