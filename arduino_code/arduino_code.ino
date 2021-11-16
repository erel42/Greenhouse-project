//Includes
#include <dht.h>

//Objects
dht DHT;

//Constants
//Define pins
#define DHT11_PIN 2
#define LDR_PIN A3
#define RELAY_1_PIN 4
#define RELAY_2_PIN 8

//Constents define
#define NUM_OF_VALUES 1 //How many values in each CSV row

//Useful variables
int i;
String input, data;

double valueArr[NUM_OF_VALUES];


//Functions

//LED control, can be removed
void LEDon();
void LEDoff();

//Handle program function
void checkInput();
void updateValues();
void sendValues();

//Sensors
void dhtUpdate();
void ldrUpdate();

//Faucet control
void turnFaucet1On();
void turnFaucet1Off();
void turnFaucet2On();
void turnFaucet2Off();



//Sensor variables
int temp = -1, humidty = -1, lightLevel = -1;

//Status variables
bool requestNewRecord = false;

void setup()
{

  pinMode(13, OUTPUT); //LED pin, can be removed
  
  //Relay pins
  pinMode(RELAY_1_PIN, OUTPUT);
    pinMode(RELAY_2_PIN, OUTPUT);

  Serial.begin(9600);
  
  Serial.println("Input 1 to Turn LED on and 2 to off"); //Can be later removed

}

void loop() {
  checkInput();
  updateValues();
  if (requestNewRecord)
    sendValues();
  delay(200);
}

void updateValues()
{
  dhtUpdate();
  ldrUpdate();
}

void dhtUpdate()
{
  int chk = DHT.read11(DHT11_PIN);
  humidty = DHT.humidity;
  temp = DHT.temperature;
}

void ldrUpdate()
{
  lightLevel = analogRead(LDR_PIN);
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

//LED control, can be removed
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

//Faucet control
void turnFaucet1On()
{
  digitalWrite(RELAY_1_PIN, LOW);
}
void turnFaucet1Off()
{
  digitalWrite(RELAY_1_PIN, HIGH);
}
void turnFaucet2On()
{
  digitalWrite(RELAY_2_PIN, LOW);
}
void turnFaucet2Off()
{
  digitalWrite(RELAY_2_PIN, HIGH);
}
