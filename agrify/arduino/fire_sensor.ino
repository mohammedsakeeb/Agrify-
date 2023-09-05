  #define SENSOR_PIN 2
#define BUZZER_PIN 3
#define RELAY_PIN 4
#define SPRINKLER_START_DELAY 2000 //5 seconds
#define SPRINKLER_ON_TIME 3000 //3 sseconds sprinkler on time

unsigned long previousTime = millis();

void setup()
{
 pinMode(RELAY_PIN, OUTPUT);
 pinMode(SENSOR_PIN, INPUT);
}

void loop()
{
 //if there is fire then the sensor value will be LOW else the value will be HIGH
 int sensorValue = digitalRead(SENSOR_PIN);

 //There is fire
 if (sensorValue == LOW)
 {
    analogWrite(BUZZER_PIN, 50);
 
    if (millis() - previousTime > SPRINKLER_START_DELAY)
    {
      digitalWrite(RELAY_PIN, LOW);
      delay(SPRINKLER_ON_TIME);
    }
 }
 else
 {
     analogWrite(BUZZER_PIN, 0);
     digitalWrite(RELAY_PIN, HIGH);
     previousTime = millis();
    }
 }
