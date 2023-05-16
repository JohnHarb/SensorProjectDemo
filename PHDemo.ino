#include "DFRobot_PH.h"
#include <EEPROM.h>
/*!
 * @file DFRobot_PH_Test.h
 * @brief This is the sample code for Gravity: Analog pH Sensor / Meter Kit V2, SKU:SEN0161-V2.
 * @n In order to guarantee precision, a temperature sensor such as DS18B20 is needed, to execute automatic temperature compensation.
 * @n You can send commands in the serial monitor to execute the calibration.
 * @n Serial Commands:
 * @n    enterph -> enter the calibration mode
 * @n    calph   -> calibrate with the standard buffer solution, two buffer solutions(4.0 and 7.0) will be automaticlly recognized
 * @n    exitph  -> save the calibrated parameters and exit from calibration mode
 *
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Jiawei Zhang](jiawei.zhang@dfrobot.com)
 * @version  V1.0
 * @date  2018-11-06
 * @url https://github.com/DFRobot/DFRobot_PH
 */
#define PH_PIN A1
const unsigned long oneHour = 6000U * 60U * 60U;//having it take the reading every hour
unsigned long current;
unsigned long startTime;
float sumPH,voltage,phValue,temperature = 25;//temp is set at 25^c to represent reef temp(temp changes ph slightly) could pull from manual inputs?

DFRobot_PH ph;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ph.begin();
}

void loop()
{
  current = millis();
  if(current - startTime >= oneHour){                  //time interval: 1 hour from last taken sample
    startTime = current;   
    for (int i = 0; i < 3; i++){
      voltage = analogRead(PH_PIN)/1024.0*5000;  // read the voltage
      phValue = ph.readPH(voltage,temperature);  // convert voltage to pH with temperature compensation
      sumPH = sumPH + phValue;                   // add new ph reading to sum
    }
    float averagePH = (sumPH / 3);             // get average from sum
    Serial.print("This Tanks PH is:");                       
    Serial.println(averagePH,2);               // print the average (Would this be better as a return for processing the average data)
  }
  sumPH = 0;
  ph.calibration(voltage,temperature);           // calibration process by Serail CMD                   
        //temperature = readTemperature();         // if we get this we can reestablish temperature reading
}