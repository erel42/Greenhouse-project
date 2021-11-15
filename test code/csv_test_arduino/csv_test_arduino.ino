String input;
int i;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  while (!Serial);

  
}

void loop() {
  // put your main code here, to run repeatedly:
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
            Serial.println("Hello from the other side");
            break;
        }
      }
      i++;
    }
  }
}
