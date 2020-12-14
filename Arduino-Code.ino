//int motorPin = 2;
int tempSensor = A1;
int ambientSensor = A0;
int LED = 2;

int ambientSensorValue = 0;
float tempSensorValue = 0;
float tempSensorValueCelcius =0;
float previousTemp = 30;
int serialData;

void setup() {
    //pinMode(motorPin, OUTPUT);
    pinMode(LED,OUTPUT);
    Serial.begin(9600);
}

void loop() {
    sendDataToSerial();
    delay(1000);
    handleLEDOnOff();
    delay(1000);
}


void sendDataToSerial(){
    handleTemperatureValue();
    handleAmbientValue();
}

//Read and print the data from the temperature sensor
    void handleTemperatureValue(){
    float averageResult =0.00;
    for (int i = 0; i < 10;i++){
      tempSensorValue = readTempSensor();
      averageResult += tempSensorValue;
      delay(10);
    }

    tempSensorValueCelcius = ((averageResult/10)*500)/1024;
    Serial.print("t," + String(tempSensorValueCelcius));
    Serial.println();
}

//Read and print the data from the the ambient light sensor
    void handleAmbientValue(){
    ambientSensorValue = analogRead(ambientSensor);
    Serial.print("a," + String(ambientSensorValue));
    Serial.println();
}

//Turn the fan on or off according to received result
void handleLEDOnOff(){
  if(Serial.available()>0)
  {
     serialData = Serial.read() - '0';

     switch (serialData){
      case 1:
        //fanOn();
        LEDOn();
        break;
      case 0:
        //fanOff();
        LEDOff();
        break;
      default:
        break;
      }
  }
}


/*void fanOff(){
    digitalWrite(motorPin, HIGH);
}

void fanOn(){
    digitalWrite(motorPin, LOW);
}
*/

void LEDOn(){
  digitalWrite(LED, HIGH);
}

void LEDOff(){
  digitalWrite(LED, LOW);
}
float readTempSensor(){
 return (analogRead(tempSensor)); 
}
