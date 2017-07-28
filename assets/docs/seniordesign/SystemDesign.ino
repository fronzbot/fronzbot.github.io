//Multidisciplinary Senior Design
//P13321 - Levitation Clock
//SystemDesign.ino - Full Levitation Clock System Implementation
//Designed by Holden Sandlar
//Revision 2 -- Completed 5/13/13

//Import Wire for I2C RTC
#include "Wire.h"
#include <stdio.h>
#include <stdlib.h>
#define DS1307_I2C_ADDRESS 0x68 //RTC I2C address

//Arduino Wire library was updated.. define I2C_READ/WRITE correctly for the version being used:
#if defined(ARDUINO) && ARDUINO >= 100   // Arduino v1.0 and newer
  #define I2C_WRITE Wire.write 
  #define I2C_READ Wire.read
#else                                   // Arduino Prior to v1.0 
  #define I2C_WRITE Wire.send 
  #define I2C_READ Wire.receive
#endif


//RGB LED Pins
#define LED_R 9
#define LED_G 10
#define LED_B 11

//Electromagnet Pins
//Looking at front of clock EM4 is MSB
#define EM4 A0
#define EM3 A1
#define EM2 A2
#define EM1 A3

//UI Pins
#define clk 12
#define rst 13

#define MI_LO 5 //DATA4
#define MI_HI 4 //DATA3
#define HR_LO 3 //DATA2
#define HR_HI 6 //DATA1

#define UI_EN 2
#define HOUR_UP 8
#define MINUTE_UP 7


// -------------------------- GLOBALS -------------------------- //

//7-Segment Digit Map
int digit_map [10][8] = {
  {0, 1, 1, 1, 1, 1, 1, 0 }, //0
  {0, 0, 1, 1, 0, 0, 0, 0 }, //1
  {0, 1, 1, 0, 1, 1, 0, 1 }, //2
  {0, 1, 1, 1, 1, 0, 0, 1 }, //3
  {0, 0, 1, 1, 0, 0, 1, 1 }, //4
  {0, 1, 0, 1, 1, 0, 1, 1 }, //5
  {0, 1, 0, 1, 1, 1, 1, 1 }, //6
  {0, 1, 1, 1, 0, 0, 0, 0 }, //7
  {0, 1, 1, 1, 1, 1, 1, 1 }, //8
  {0, 1, 1, 1, 0, 0, 1, 1 } //9
};



byte hour, second, minute;
char zero = 0x00;
byte temp_hour, temp_minute, temp_second;

volatile boolean USER_INPUT_FLAG;
volatile boolean DEMO_MODE;
int hour_input, minute_input;
byte saved_hour, saved_minute; // used when not in UI mode
static unsigned long last_interrupt_time;
// ------------------------- END GLOBALS ---------------------- //


void setup()
{
  //Initially not in UI or DEMO mode
  USER_INPUT_FLAG = false;
  DEMO_MODE = false;
  
  //Setup RGB and Electromagnet pins as output pins
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(EM1, OUTPUT);
  pinMode(EM2, OUTPUT);
  pinMode(EM3, OUTPUT);
  pinMode(EM4, OUTPUT);
  
  //Setup UI clock and reset as output pins
  pinMode(clk, OUTPUT);
  pinMode(rst, OUTPUT); //active low
  
  //Setup UI data pins as output pins
  pinMode(HR_HI, OUTPUT);
  pinMode(HR_LO, OUTPUT);
  pinMode(MI_HI, OUTPUT);
  pinMode(MI_LO, OUTPUT);
  
  //Setup UI buttons as input pins
  pinMode(UI_EN, INPUT);
  pinMode(HOUR_UP, INPUT);
  pinMode(MINUTE_UP, INPUT);
  
  //Start the I2C Interface
  Wire.begin();

  //Initially all signals set HIGH
  digitalWrite(rst, HIGH);  
  digitalWrite(clk, HIGH);
  digitalWrite(HR_HI, HIGH);
  digitalWrite(HR_LO, HIGH);
  digitalWrite(MI_HI, HIGH);
  digitalWrite(MI_LO, HIGH);

  //On power up green LED on
  analogWrite(LED_R, 0);
  analogWrite(LED_G, 255);
  analogWrite(LED_B, 0);
  
  resetEM(); //Turn off all electromagnet drivers
  resetDisp(); //Reset shift registers
  setTimeOnRTC(12,00); //Set time to 12:00 on RTC (system power up)
  getTimeOnRTC(); //Get the current time (12:00) -- sets up initial values for globals
  
}

void loop()
{
  //Check if in user input mode
  //If yes (in UI mode) - call drive hours to zero 
  //If no - if changed from last run, drive electromagnet changes, drive minute changes
  getDemoFlag(); //Get DEMO flag -- checks if all 3 buttons are pushed
  if(!DEMO_MODE) 
  {
    //Not in demo mode.. check for user input and display the time
    getUIFlag();
    if(!USER_INPUT_FLAG)
    {
      getTimeOnRTC(); //Get current time from RTC
      temp_hour = bcdToDec(hour);
      temp_minute = bcdToDec(minute);  
      
      //resetDisp(); //Clear anything currently in the shift registers
      if(temp_hour > 12) {
        temp_hour = 1; //If decimal hour returned > 12, subtract 12 to only display 12-hour time format
        setTimeOnRTC(temp_hour, temp_minute);
      }
      if(temp_hour == 0) temp_hour = 12; //If decimal hour returned == 0, it is 12 AM
      
      
      if(temp_hour != saved_hour || temp_minute != saved_minute)
      {
        //Serial.println(hour,BIN); // DEBUG
        saved_hour = temp_hour;
        saved_minute = temp_minute;
    
        //Display current time on 7-segs
  
        resetDisp();
        shift_number_in(decToBcd(temp_hour)>>4, decToBcd(temp_hour)&0x0F, decToBcd(temp_minute)>>4, decToBcd(temp_minute) &0x0F);
        displayHours(temp_hour);
        displayMinutes(temp_minute);
        delay(50);
      }
      else
      {
        saved_hour = temp_hour;
        saved_minute = temp_minute;
      }
      
      delay(100);
    }
    else
    {
      //In user-input mode
      //we want to read from buttons to update display
      
      getTimeOnRTC();
      int changed = 0;
      temp_hour = bcdToDec(hour);
      temp_minute = bcdToDec(minute);  
      
      hour_input = !digitalRead(HOUR_UP);
      minute_input = !digitalRead(MINUTE_UP);
      if(hour_input) { temp_hour++; changed = 1; } //If user has pressed hour_input button, increase hour
      if(minute_input) { temp_minute++; changed = 1; } //If user has pressed minute_input button, increase minute
      if(temp_hour > 12) { temp_hour -= 12; changed = 1; } //If user rolls over 12 hours, reset to 01
      if(temp_minute == 60) { temp_minute = 0; changed = 1; } //If minute == 60, roll over to 00
        
      //Save new time to RTC
      if (changed){
        setTimeOnRTC(decToBcd(temp_hour), temp_minute);
      }
      
      resetDisp(); //Clear display.. want to blink if it is in user input mode
      delay(250); //Blink duration
      
      //Display New User time
      shift_number_in(decToBcd(temp_hour)>>4, decToBcd(temp_hour)&0x0F, decToBcd(temp_minute)>>4, decToBcd(temp_minute) &0x0F);
      
      
      delay(400); //On time duration.. also restricts time between subsequent hour/min button presses
    }
  }
  else
  {
    //In demo mode.. increase the minute every second
    getTimeOnRTC(); //Get current time from RTC
    temp_hour = bcdToDec(hour);
    temp_minute = bcdToDec(minute);  
    
    //resetDisp(); //Clear anything currently in the shift registers
    if(temp_hour > 12) {
      temp_hour = 1; //If decimal hour returned > 12, subtract 12 to only display 12-hour time format
      setTimeOnRTC(temp_hour, temp_minute);
    }
    if(temp_hour == 0) temp_hour = 12; //If decimal hour returned == 0, it is 12 AM
    
    
    if(temp_hour != saved_hour || temp_minute != saved_minute)
    {
      //Serial.println(hour,BIN); // DEBUG
      saved_hour = temp_hour;
      saved_minute = temp_minute;
  
      //Display current time on 7-segs

      resetDisp();
      shift_number_in(decToBcd(temp_hour)>>4, decToBcd(temp_hour)&0x0F, decToBcd(temp_minute)>>4, decToBcd(temp_minute) &0x0F);
      displayHours(temp_hour);
      displayMinutes(temp_minute);
      delay(5);
      //USER_INPUT_FLAG = false;
    }
    else
    {
      saved_hour = temp_hour;
      saved_minute = temp_minute;
    }
    delay(1000);
    if(temp_minute == 59) setTimeOnRTC(temp_hour+1, 0);
    else setTimeOnRTC(temp_hour, temp_minute+1);
  }
}

//Turn off drivers for all electromagnets
void resetEM()
{ 
  digitalWrite(EM1, LOW);
  digitalWrite(EM2, LOW);
  digitalWrite(EM3, LOW);
  digitalWrite(EM4, LOW);  
}

// Gets the date and time from the ds1307
void getTimeOnRTC()
{
  // Reset the register pointer
  Wire.beginTransmission(DS1307_I2C_ADDRESS); //Start transmision
  I2C_WRITE(zero); //Write 0x00 to register pointer (points to register to read in RTC memory space)
  Wire.endTransmission(); //End transmission
 
  Wire.requestFrom(DS1307_I2C_ADDRESS, 3); //Start a transaction to read 7 bytes from the RTC starting at RTC register 0x00 (set in previous command)
 
  
  second  = bcdToDec(I2C_READ() & 0x7f); //MSB is a Clock Halt bit. Mask this off.
                                         //Seconds in format S7 S6 S5 S4 S3 S2 S1
                                         //S7-S5 represents 10's of seconds (ex. 40 seconds would be 010)
                                         //S4-S1 represents 1's of seconds (ex. 5 seconds would be 0101)
  minute = I2C_READ(); //Minutes in format M8 M7 M6 M5 M4 M3 M2 M1
                       //M8 is always 0
                       //M7-M5 represents 10's of minutes
                       //M4-M1 represents 1's of minutes
  
  hour = bcdToDec(I2C_READ() & 0x3f); //Hours in format H8 H7 H6 H5 H4 H3 H2 H1
                                      //H8 is always 0 -- masked here
                                      //H7 Indicates 12 hour or 24 hour format -- configure this for 24 hour - This bit set LOW
                                      //H6-H5 Indicates 10's of hours -- (ex. 12:00 would be represented as 01 (bin), 24:00 would be represented as 10 (bin))
                                      //H4-H1 Indicates 1's of hours -- (ex. 5:00 would be 0101 (bin), 13:00 would be 0011)
}

//Function setTimeOnRTC
//Takes integer hour and minute and writes the new time to the RTC
void setTimeOnRTC(byte hr_in, byte mn_in)
{
   Wire.beginTransmission(DS1307_I2C_ADDRESS); //Start I2C transaction
   I2C_WRITE(zero); //Reset R/W RTC internal pointer
   I2C_WRITE(decToBcd(0x00) & 0x7f);    // Set seconds to 00
   I2C_WRITE(decToBcd(mn_in));       //Set minutes to mn_in
   I2C_WRITE(decToBcd(hr_in));      // Set hours to hr_in
                                   
   Wire.endTransmission(); //Close I2C transaction
}

//Converts a decimal number to a BCD number
byte decToBcd(byte val)
{
  return ( (val/10*16) + (val%10) );
}
 
// Convert binary coded decimal to normal decimal numbers
byte bcdToDec(byte val)
{
  return ( (val/16*10) + (val%16) );
}

//Resets data in all shift registers
void resetDisp()
{
  digitalWrite(rst,LOW);
  delay(1);
  digitalWrite(rst,HIGH);
}


//Function: shift_number_in ( hour_high_digit, hour_low_digit, minute_high_digit, minute_low_digit )
void shift_number_in(int hour_hi, int hour_lo, int min_hi, int min_lo)
{
  //Shift in eight bits to each shift register. Output of shift registers is hooked up to 7-segs.
  for(int i = 0; i<9; i++)
  {
    digitalWrite(HR_HI, digit_map[hour_hi][i]); 
    if(i == 8) digitalWrite(HR_LO, HIGH);
    else digitalWrite(HR_LO, digit_map[hour_lo][i]);
    digitalWrite(MI_HI, digit_map[min_hi][i]);
    digitalWrite(MI_LO, digit_map[min_lo][i]);
    
    //Clock this data in
    clock();
  }
  
}

void toggle_user_input_flag()
{
  last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > 500) 
  {
    USER_INPUT_FLAG = !USER_INPUT_FLAG;    
  }
  last_interrupt_time = interrupt_time;
}

void clock()
{
      //Clock this data in
    
    digitalWrite(clk, LOW);
    delayMicroseconds(3);
    digitalWrite(clk, HIGH);
    delayMicroseconds(3);
  
}

void driveRGB(int red, int green, int blue)
{
  analogWrite(LED_R, red);
  analogWrite(LED_G, green);
  analogWrite(LED_B, blue);
}

//Function displayMinutes(minute)
//Essentially LUT to drive the RGB LED
void displayMinutes(int minute)
{
  if (minute >= 0 && minute < 5) driveRGB(204,0,0);
  else if(minute >=5 && minute < 10) driveRGB(204,102,0);
  else if(minute >=10 && minute < 15) driveRGB(204,204,0);
  else if(minute >=15 && minute < 20) driveRGB(102,204,0);
  else if(minute >=20&& minute < 25) driveRGB(0,204,0);
  else if(minute >=25 && minute < 30) driveRGB(0,204,102);
  else if(minute >=30 && minute < 35) driveRGB(0,204,204);
  else if(minute >=35 && minute < 40) driveRGB(0,102,204);
  else if(minute >=40 && minute < 45) driveRGB(0,0,204);  
  else if(minute >=45 && minute < 50) driveRGB(102,0,204);
  else if(minute >=50 && minute < 55) driveRGB(204,0,204);
  else if(minute >=55 && minute < 60) driveRGB(204,0,102);
}

//Functon displayHours(hour)
//Essentially LUT to drive the electromagnets
void displayHours(int hour)
{
  switch(hour)
  {
    case 1:
      digitalWrite(EM1,1);
      digitalWrite(EM2,0);
      digitalWrite(EM3,0);
      digitalWrite(EM4,0);
      break;
    case 2:
      digitalWrite(EM1,0);
      digitalWrite(EM2,1);
      digitalWrite(EM3,0);
      digitalWrite(EM4,0);
      break;
    case 3:
      digitalWrite(EM1,1);
      digitalWrite(EM2,1);
      digitalWrite(EM3,0);
      digitalWrite(EM4,0);
      break;
    case 4:
      digitalWrite(EM1,0);
      digitalWrite(EM2,0);
      digitalWrite(EM3,1);
      digitalWrite(EM4,0);
      break;
    case 5:
      digitalWrite(EM1,1);
      digitalWrite(EM2,0);
      digitalWrite(EM3,1);
      digitalWrite(EM4,0);
      break;
    case 6:
      digitalWrite(EM1,0);
      digitalWrite(EM2,1);
      digitalWrite(EM3,1);
      digitalWrite(EM4,0);
      break;
    case 7:
      digitalWrite(EM1,1);
      digitalWrite(EM2,1);
      digitalWrite(EM3,1);
      digitalWrite(EM4,0);
       break;
    case 8:
      digitalWrite(EM1,0);
      digitalWrite(EM2,0);
      digitalWrite(EM3,0);
      digitalWrite(EM4,1);
       break;
    case 9:
      digitalWrite(EM1,1);
      digitalWrite(EM2,0);
      digitalWrite(EM3,0);
      digitalWrite(EM4,1);
       break;
    case 10:
       digitalWrite(EM1,0);
      digitalWrite(EM2,1);
      digitalWrite(EM3,0);
      digitalWrite(EM4,1);
       break;
    case 11:
      digitalWrite(EM1,1);
      digitalWrite(EM2,1);
      digitalWrite(EM3,0);
      digitalWrite(EM4,1);
       break;
    case 12:
      digitalWrite(EM1,0);
      digitalWrite(EM2,0);
      digitalWrite(EM3,1);
      digitalWrite(EM4,1);
       break; 
    default:
      digitalWrite(EM1,0);
      digitalWrite(EM2,0);
      digitalWrite(EM3,0);
      digitalWrite(EM4,0);
      break;
     
  }
}
//Function getUIFlag
//Checks if UI enable button being held down
void getUIFlag()
{
  USER_INPUT_FLAG = !digitalRead(UI_EN);
}

//Function getDemoFlag
//Checks if all three buttons pressed (demo mode entered)
//If currently in demo mode, checks if any button pressed (exiting demo mode)
void getDemoFlag()
{
  int flag1 = !digitalRead(UI_EN);
  int flag2 = !digitalRead(HOUR_UP);
  int flag3 = !digitalRead(MINUTE_UP);
  if(DEMO_MODE) 
  {
    if (flag1 == 1 || flag2 == 1 || flag3 == 1) DEMO_MODE = false;
  }
  else
  {
  if(flag1 == 1 && flag2 == 1 && flag3 == 1)
   {
     DEMO_MODE = true;
   }
  } 
}
