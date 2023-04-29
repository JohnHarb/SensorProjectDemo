#include "DFRobot_PH.h"

#define PH_PIN A1
const unsigned long oneHour = 1000UL * 60 * 60; //having it take the reading every hour
float sumPH,voltage,phValue,temperature = 25;//temp is set at 25^c to represent reef temp(temp changes ph slightly) could pull from manual inputs?
unsigned long lastTaken = 0 - oneHour;
DFRobot_PH ph;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop()
{
    static unsigned long current = millis();
    if(current - lastTaken >= oneHour){                  //time interval: 1 hour from last taken sample
        lastTaken += oneHour;                      //establish new last taken sample
        int count;
        //temperature = readTemperature();         // if we get this we can reestablish temperature reading
        for (int i = 0; i < count; i++){
        voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
        phValue = ph.readPH(voltage,temperature);  // convert voltage to pH with temperature compensation
        sumPH = sumPH + phValue;                   // add new ph reading to sum
        }
        float averagePH = (sumPH / (float)count);  // get average from sum
        Serial.print("pH:");                       
        Serial.println(averagePH,2);               // print the average (Would this be better as a return for processing the average data)
    }
    ph.calibration(voltage,temperature);           // calibration process by Serail CMD
}