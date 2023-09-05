int sensor_pin = A0; // Soil Sensor input at Analog PIN A0
int output_value ;
void setup() {
  // put your setup code here, to run once:
  pinMode(7,OUTPUT);
     Serial.begin(9600);
  
   delay(2000);
}


  // put your main code here, to run repeatedly:

  void loop() {
   output_value= analogRead(sensor_pin);
 output_value = map(output_value,550,10,0,100);
   Serial.print("Mositure : ");
   Serial.print(output_value);
   Serial.println("%");
   if(output_value<0 or output_value>70 ){
      digitalWrite(7,HIGH);
     }
    

     else
     {
            digitalWrite(7,LOW);
     }
   delay(1000);
}
