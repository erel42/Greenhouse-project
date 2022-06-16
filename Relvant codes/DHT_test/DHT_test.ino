/* How to use the DHT-11 sensor with Arduino uno
   Temperature and humidity sensor
   More info: http://www.ardumotive.com/how-to-use-dht-11-sensor-en.html
   Dev: Michalis Vasilakis // Date: 2/7/2015 // www.ardumotive.com */

//Libraries
#include <dht.h>
dht DHT;
//Constants
#define DHT11_PIN 2

#define LDR_PIN A3

#define RELAY_1_PIN 4
#define RELAY_2_PIN 8

//Variables
float hum = -1;  //Stores humidity value
float temp = -1; //Stores temperature value

int lightLevel = -1;

bool relay1Status = true;
bool relay2Status = true;

void setup()
{
    Serial.begin(9600);
    pinMode(RELAY_1_PIN, OUTPUT);
    pinMode(RELAY_2_PIN, OUTPUT);
}

void loop()
{
    int chk = DHT.read11(DHT11_PIN);
    //Read data and store it to variables hum and temp
    hum = DHT.humidity;
    temp= DHT.temperature;
    //Print temp and humidity values to serial monitor
    Serial.print("Humidity: ");
    Serial.print(hum);
    Serial.print(" %, Temp: ");
    Serial.print(temp);
    Serial.println(" Celsius");
  
    lightLevel = analogRead(LDR_PIN);
    Serial.println(lightLevel);

    digitalWrite(RELAY_1_PIN, relay1Status);
    digitalWrite(RELAY_2_PIN, relay2Status);

    delay(2000); //Delay 2 sec.
}
