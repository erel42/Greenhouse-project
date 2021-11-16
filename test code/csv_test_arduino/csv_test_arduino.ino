String input;
int i;
int finished = false;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  while (!Serial);
  Serial.print("rHello,from,the,other,side]");
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (Serial.available())
  {
    input = Serial.readString();
    i = 0;
    Serial.println(input);
    finished = false;
    while(!finished && i < input.length())
    {
      if(input[i] > '0' && input[i] < 'z')
      {
        switch(input[i])
        {
          case ('1'): //LED on
            Serial.println("rHello,from,the,other,side");
            finished = true;
            break;
        }
      }
      i++;
    }
  }
}
