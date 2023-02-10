#include "DFRobot_PH.h"

#define PH_PIN A1
float voltage,phValue,temperature = 25;
DFRobot_PH ph;

void setup() {
  // put your setup code here, to run once:

}

void loop()
{
    static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U){                  //time interval: 1s
        timepoint = millis();
        //temperature = readTemperature();         // read your temperature sensor to execute temperature compensation
        voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
        phValue = ph.readPH(voltage,temperature);  // convert voltage to pH with temperature compensation
        Serial.print("temperature:");
        Serial.print(temperature,1);
        Serial.print("^C  pH:");
        Serial.println(phValue,2);
    }
    ph.calibration(voltage,temperature);           // calibration process by Serail CMD
}