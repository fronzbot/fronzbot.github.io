/*
    Infrared Proximity Sensor Distance Detection v1.0
    For use with Infrared Proximity Sensor Schematic v1.2
    By: Kevin Fronczak
    
    Code uses a mix of AVR and Arduino for readability and ease of use
*/

#define  ADC                A0        // ADC Input pin
#define  three_inches       780       // Threshold for 3 inchs
#define  six_inches         670       // Threshold for 6 Inches
#define  nine_inches        590       // Threshold for 9 Inchs

int adc_reading = 0;

void setup()
{
  DDRD = 0x3C;                  // Set digital output pins as 4, 5, 6, 11
  DDRC = 0x1;                   // Set ADC Input pin 23
  analogReference(DEFAULT);          
  Serial.begin(19200);          // For debugging
}

int sensVal;                    // for raw sensor values 
float filterVal = 0.99;         // this determines smoothness  - .0001 is max  1 is off (no smoothing)
float smoothedVal;              // this holds the last loop value just use a unique variable for every different sensor that needs smoothing
float smoothedVal2;             // this would be the buffer value for another sensor if you needed to smooth two different sensors - not used in this sketch
int i, j;                       // loop counters or demo     


void loop()
{ 
  for (j = 0; j< 60; j++){      
    if (j < 30){                  // generate a simulated square wave
      sensVal = 1023;
    }
    else
    {
      sensVal = 0; 
    }
    sensVal = analogRead(ADC); 
    adc_reading =  smooth(sensVal, filterVal, adc_reading);   // second parameter determines smoothness  - 0 is off,  .9999 is max smooth 
  }

  Serial.println(adc_reading);      // For debugging
  if(adc_reading > three_inches)
  {
    PORTD &= ~(0x3C);   // Turn LEDs off
    PORTD |= 0x4;       // Turn <3" LED on
  }
  else if(adc_reading > six_inches && adc_reading <= three_inches)
  {
    PORTD &= ~(0x3C);   // Turn LEDs off
    PORTD |= 0x8;       // Turn 3"-6" LED on
  }
  else if(adc_reading > nine_inches && adc_reading <= six_inches)
  {
    PORTD &= ~(0x3C);   // Turn LEDs off
    PORTD |= 0x10;       // Turn 6"-9" LED on
  }
  else if(adc_reading < nine_inches)
  {
    PORTD &= ~(0x3C);   // Turn LEDs off
    PORTD |= 0x20;      // Turn >9" LED on
  } 
}

/*
  Digital filter to smooth input of ADC
*/
int smooth(int data, float filterVal, float smoothedVal){
  if (filterVal > 1){      // check to make sure param's are within range
    filterVal = .99;
  }
  else if (filterVal <= 0){
    filterVal = 0;
  }
  smoothedVal = (data * (1 - filterVal)) + (smoothedVal  *  filterVal);
  return (int)smoothedVal;
}
