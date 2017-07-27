/*
 * 10 bit ADC
 * 1 inch  --> 0x35D --> 861
 * 2 inch  --> 0x356 --> 854
 * 3 inch  --> 0x252 --> 594
 * 4 inch  --> 0x1E2 --> 482
 * 5 inch  --> 0x17C --> 380
 * 6 inch  --> 0x15B --> 347
 * 7 inch  --> 0x146 --> 326
 * 8 inch  --> 0x135 --> 309
 * 9 inch  --> 0x123 --> 291
 * 10 inch --> 0x11E --> 286
 * 11 inch --> 0x118 --> 280
 * 12 inch --> 0x115 --> 277
 *
 * 1 < d < 6  ----  4720*(ADC_VAL)^-1.15
 *
 * 6 <= d <= 9  ----  -0.054*(ADC_VAL) + 24.7
 *
 * d > 9  ----  -0.22*(ADC_VAL) + 71.2
 *
 * All distance (except 1 inch)
 * 53090*(ADC_VAL)^-1.5
 *
 */

#include "msp430g2231.h"

#define one_inch	0x332
#define two_inch 	0x224
#define three_inch 	0x13E
#define four_inch 	0x11A
#define five_inch 	0x11A
#define six_inch 	0xFF
#define seven_inch 	0xF8
#define eight_inch 	0xF3
#define nine_inch 	0xE1

volatile double temp_ADC;
volatile double val;
volatile double estimated_dist;
volatile int dist;
volatile int led_flag;


void calculateDistance(int ADC_Reading)
{
	temp_ADC = (double)ADC_Reading;

	if (ADC_Reading >= three_inch)//0x184
	{
		led_flag = 1;
	}
	else if (ADC_Reading >= six_inch && ADC_Reading < three_inch)//0xCF, 0x1E2
	{
		led_flag = 2;
	}
	else if (ADC_Reading >= nine_inch && ADC_Reading < six_inch)
	{
		led_flag = 3;
	}
	else if (ADC_Reading < nine_inch)
	{
		led_flag = 4;
	}
	else
	{
		led_flag = 0;
	}
	switch(led_flag)
	{
	case 0:
		P1OUT &= ~(0x4|0x8|0x10|0x20);
		P1OUT |= 0x1;
		break;
	case 1:
		P1OUT &= ~(0x8|0x10|0x20);
		P1OUT |= 0x4;
		break;
	case 2:
		P1OUT &= ~(0x4|0x10|0x20);
		P1OUT |= 0x8;
		break;
	case 3:
		P1OUT &= ~(0x4|0x8|0x20);
		P1OUT |= 0x10;
		break;
	case 4:
		P1OUT &= ~(0x4|0x8|0x10);
		P1OUT |= 0x20;
		break;
	default:
		P1OUT &= ~(0x4|0x8|0x10|0x20);
		break;

	}

}

void main(void)
{
	int ADC_Value = 0;
	WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT
	ADC10CTL0 = ADC10SHT_2 + ADC10ON + ADC10IE; // ADC10ON, interrupt enabled
	ADC10CTL1 = INCH_1;                       // input A1
	ADC10AE0 |= 0x02;                         // PA.1 ADC option select
	P1DIR |= 0x3C;               			// Set P1.2-1.5 to output
	P1DIR |= 0x1;
	for (;;)
	{
		ADC10CTL0 |= ENC + ADC10SC +REFON;             // Sampling and conversion start
		__bis_SR_register(CPUOFF + GIE);        // LPM0, ADC10_ISR will force exit
		int i;
		for (i = 0; i < 32; ++i)				// Average 25 readings to get more stable ADC Value
		{
			ADC_Value += ADC10MEM;
		}
		ADC_Value = ADC_Value/32;
		calculateDistance(ADC_Value);
		/*
		if (ADC10MEM < 0x1FF)
			P1OUT &= ~0x01;
		else
			P1OUT |= 0x01;
		if (ADC10MEM < 0x3E0)
			P1OUT &= ~0x40;
		else
			P1OUT |= 0x40;
			*/

	}
}

// ADC10 interrupt service routine
#pragma vector=ADC10_VECTOR
__interrupt void ADC10_ISR(void)
{
	__bic_SR_register_on_exit(CPUOFF);        // Clear CPUOFF bit from 0(SR)
}
