//#include <avr/sleep.h>
//#include <avr/power.h>
//
//volatile int f_timer=0;
//ISR(TIMER1_OVF_vect)
//{
//  /* set the flag. */
//   if(f_timer == 0)
//   {
//     f_timer = 1;
//   }
//}
//void enterSleep(void)
//{
//  set_sleep_mode(SLEEP_MODE_IDLE);
//  
//  sleep_enable();
//
//
//  /* Disable all of the unused peripherals. This will reduce power
//   * consumption further and, more importantly, some of these
//   * peripherals may generate interrupts that will wake our Arduino from
//   * sleep!
//   */
//  power_adc_disable();
//  power_spi_disable();
//  power_timer0_disable();
//  power_timer2_disable();
//  power_twi_disable();  
//
//  /* Now enter sleep mode. */
//  sleep_mode();
//  
//  /* The program will continue from here after the timer timeout*/
//  sleep_disable(); /* First thing to do is disable sleep. */
//  
//  /* Re-enable the peripherals. */
//  power_all_enable();
//}
void setup() {
  pinMode(11, OUTPUT);
  digitalWrite(11, LOW);
  Serial.begin(9600);
  /*** Configure the timer.***/
  
  /* Normal timer operation.*/
  //TCCR1A = 0x00; 
  
  /* Clear the timer counter register.
   * You can pre-load this register with a value in order to 
   * reduce the timeout period, say if you wanted to wake up
   * ever 4.0 seconds exactly.
   */
  //TCNT1=0x7530; 
  
  /* Configure the prescaler for 1:1024, giving us a 
   * timeout of 4.09 seconds.
   */
  //TCCR1B = 0x05;
  
  /* Enable the timer overlow interrupt. */
  //TIMSK1=0x01;
}

//char buffer [255];
int av1,av2,av3;
int tav1,tav2,tav3;
void loop() {
//  if(f_timer==1)
//  {
//    f_timer = 0;
      
  av1 = analogRead(A0);
  av2 = analogRead(A1);
  av3 = analogRead(A2);
  tav1 = av1;
  tav2 = av2-av1;
  tav3 = av3-av2-av1;
  
  if(tav1<=256 ||tav2<=256 ||tav3<=256){ //256 corresponds to 3.75 volts
    digitalWrite(11,HIGH);
    delay(500);
  }
  else {
      digitalWrite(11,LOW);
  }
      if(Serial){
        float cell1 = tav1 * (15.0 / 1023.0);
        float cell2 = tav2 * (15.0 / 1023.0);
        float cell3 = tav3 * (15.0 / 1023.0);
      //sprintf (buffer, "%e - %e - %e",cell1,cell2,cell3);
      //Serial.println(buffer);
      Serial.println("_______________");
      Serial.print("cell1 ");
      Serial.println(cell1);
      Serial.print("cell2 ");
      Serial.println(cell2);
      Serial.print("cell3 ");
      Serial.println(cell3);
      Serial.println("----------------");
      }
      //Serial.print(" cell1 ");
      //Serial.print(cell1);
      //Serial.print(" cell2 ");
      //Serial.print(cell2);
      //Serial.print(" cell3 ");
      //Serial.print(cell3);
      //Serial.println();
  //enterSleep();
  //}
}
