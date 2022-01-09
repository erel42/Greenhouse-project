#define VERSION "V 1.0.0"

//Includes
#include <DHT.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>


//Define pins
#define dht_pin 2
#define DHTTYPE DHT11
#define LDR_PIN A3
#define RELAY_1_PIN 4
#define RELAY_2_PIN 8
#define MOIST_SENSOR_PIN A1
#define PH_SENSOR_PIN A0

//Constents define
#define NUM_OF_VALUES 5 //How many values in each CSV row
#define LCD_pages 2
#define LCD_ROUNDS 6

//Objects
DHT dht(dht_pin, DHTTYPE);
LiquidCrystal_I2C lcd(0x27,20,4);

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

//LCD
void lcdCycle();

//RGB strip
void setColor(String data, int start);

//Useful variables
int i, cycle = 0, rounds = 0;
String input, data, tmp;
int RGB[3] = {0,0,0};
bool leave = false;

//Sensor variables
float temp = -1, humidty = -1, moist = -1, light = -1, pH_Value = -1, RLDR = 0, Vout = 0;
int lightLevel = -1;
int red = 0, green = 0, blue = 0; //RGB values

//Status variables
bool relay1status = true; //faucet is off
bool relay2status = true;
bool printed = false;

void setup()
{
  lcd.init();                      // initialize the lcd 
  // Print a message to the LCD.
  lcd.backlight();
  
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.write(VERSION);
  
  pinMode(13, OUTPUT); //LED pin, can be removed
  
  //Relay pins
  pinMode(PH_SENSOR_PIN, INPUT); 
  pinMode(RELAY_1_PIN, OUTPUT);
  pinMode(RELAY_2_PIN, OUTPUT);
  digitalWrite(RELAY_1_PIN, HIGH);
  digitalWrite(RELAY_2_PIN, HIGH);

  dht.begin();
  Serial.begin(9600);
}

void loop() {
  checkInput();
  updateValues();
  lcdCycle();
  sendValues();
  delay(2000);
}

void updateValues()
{
  dhtUpdate();
  ldrUpdate();
  moist = analogRead(MOIST_SENSOR_PIN); 
  valueArr[3] = moist;
  pH_Value = analogRead(PH_SENSOR_PIN);
  valueArr[4] = pH_Value;

}

void lcdCycle()
{
  rounds++;

  //First screen, Sendor values (excluding ph)
  if(cycle == 0)
  {
    //Const print
    if(!printed)
    {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Tempature: ");
      lcd.setCursor(0,1);
      lcd.print("Humidity: ");
      lcd.setCursor(0,2);
      lcd.print("Light: ");
      lcd.setCursor(0,3);
      lcd.print("Moisture: ");

      lcd.setCursor(17,0);
      lcd.print("C");
      lcd.setCursor(17,1);
      lcd.print("%");
      lcd.setCursor(17,2);
      lcd.print("LUX");
      lcd.setCursor(17,3);
      lcd.print("%");
      
      printed = true;
    }

    //Clear loop
    for(i = 0; i < 4; i++)
    {
      lcd.setCursor(10,i);
      lcd.print("       ");
    }

    //Tempature
    if(temp >= 100)
      lcd.setCursor(11,0);
    else if (temp >= 10)
      lcd.setCursor(12,0);
    else
      lcd.setCursor(13,0);
    lcd.print(temp);

    //Humidity
    if(humidty >= 100)
      lcd.setCursor(11,1);
    else if (humidty >= 10)
      lcd.setCursor(12,1);
    else
      lcd.setCursor(13,1);
    lcd.print(humidty);

    //Light
    if (light >= 1000)
      lcd.setCursor(10,2);
    else if(light >= 100)
      lcd.setCursor(11,2);
    else if (light >= 10)
      lcd.setCursor(12,2);
    else
      lcd.setCursor(13,2);
    lcd.print(light);

    //Moistrue
    if(moist >= 100)
      lcd.setCursor(11,3);
    else if (moist >= 10)
      lcd.setCursor(12,3);
    else
      lcd.setCursor(13,3);
    lcd.print(moist);
  }
  else if (cycle == 1)
  {
    if(!printed)
    {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("PH: ");
      lcd.setCursor(0,1);
      lcd.print("Valve 1: ");
      lcd.setCursor(0,2);
      lcd.print("Valve 2: ");
      
      lcd.setCursor(17,0);
      lcd.print("ph");

      lcd.setCursor(0,3);
      lcd.print("R: ");

      lcd.setCursor(7,3);
      lcd.print("G: ");

      lcd.setCursor(14,3);
      lcd.print("B: ");
      
      printed = true;
    }

    //Clear loop
    for(i = 0; i < 3; i++)
    {
      lcd.setCursor(10,i);
      lcd.print("       ");
    }

	//pH
	lcd.setCursor(14,1);
    lcd.print(pH_Value);

    //Faucet 1
    lcd.setCursor(12,1);
    if(relay1status)
      lcd.print("Close");
    else
      lcd.print("Open");

    //Faucet 2
    lcd.setCursor(12,2);
    if(relay2status)
      lcd.print("Close");
    else
      lcd.print("Open");

    //RGB vaules
    lcd.setCursor(3,3);
    lcd.print("   ");
    if (red >= 100)
      lcd.setCursor(3,3);
    else if (red >= 10)
      lcd.setCursor(4,3);
    else
      lcd.setCursor(5,3);
    lcd.print(red);

    lcd.setCursor(10,3);
    lcd.print("   ");
    if (green >= 100)
      lcd.setCursor(10,3);
    else if (green >= 10)
      lcd.setCursor(11,3);
    else
      lcd.setCursor(12,3);
    lcd.print(green);

    lcd.setCursor(17,3);
    lcd.print("   ");
    if (blue >= 100)
      lcd.setCursor(17,3);
    else if (blue >= 10)
      lcd.setCursor(18,3);
    else
      lcd.setCursor(19,3);
    lcd.print(blue);
  }
  
  if (rounds >= LCD_ROUNDS)
  {
    rounds = 0;
    printed = false;
    cycle++;
  }
  if(cycle >= LCD_pages)
  {
    cycle = 0;
  }
}

void dhtUpdate()
{
  humidty = dht.readHumidity();
  temp = dht.readTemperature();
  valueArr[0] = temp;
  valueArr[1] = humidty;
}

void ldrUpdate()
{
  lightLevel = analogRead(LDR_PIN);
  Vout = (ADC * 0.0048828125);                

  light = (2500/Vout-500)/10;
  valueArr[2] = light;
}

void sendValues()
{
  data = "r";
  data += valueArr[0];
  for(i = 1; i < NUM_OF_VALUES; i++)
  {
    data += ",";
    data += valueArr[i];
  }
  data += "]";
  Serial.println(data);
}

void checkInput()
{ //Needs rework
  if (Serial.available())
  {
    input = Serial.readString();
    i = 0;
    while(i < input.length() && !leave)
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
          case ('3'): //LED off
            turnFaucet1On();
            break;
          case ('4'): //LED off
            turnFaucet1Off();
            break;
          case ('5'): //LED off
            turnFaucet2On();
            break;
          case ('6'): //LED off
            turnFaucet2Off();
            break;
          case('c'):
            setColor(input, i + 2);
            leave = true;
            break;
        }
      }
      i++;
    }
    leave = false;
  }
}

//RGB strip control
void setColor(String data, int start)
{
  tmp = "";
  i = 0;
  for(; start < data.length(); start++)
  {
   if(data[start] != ' ' && data[start] != '\n')
    tmp += data[start];
   else
   {
    RGB[i] = tmp.toInt();
    tmp = "";
    if (RGB[i] > 255 || RGB[i] < 0)
      return;
    i++;
   }
  }
  red = RGB[0];
  green = RGB[1];
  blue = RGB[2];
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
  relay1status = false;
  digitalWrite(RELAY_1_PIN, relay1status);
}
void turnFaucet1Off()
{
  relay1status = true;
  digitalWrite(RELAY_1_PIN, relay1status);
}
void turnFaucet2On()
{
  relay2status = false;
  digitalWrite(RELAY_2_PIN, relay2status);
}
void turnFaucet2Off()
{
  relay2status = true;
  digitalWrite(RELAY_2_PIN, relay2status);
}
