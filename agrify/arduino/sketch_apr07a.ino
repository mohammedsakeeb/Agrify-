
int sensor1 = A3;

String datalabel1 = "temperature";

  int voltage = sensor1 * (5.0 /3000.0);

  // Convert the voltage into the temperature in Celsius
int data1 = voltage * 100;
bool label = true;


void setup() {
  // Begin serial communication at 9600 baud rate
  Serial.begin(9600);
  pinMode(sensor1,INPUT);
    
}

void loop() {

while(label){
  Serial.println(datalabel1);

  label = false;
    
}
   data1 = analogRead(sensor1);
   data1=data1-63;

   Serial.println(data1);


   delay(1000);
   
}
