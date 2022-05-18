/************************************************************
 * Description: Serial Communication to Raspi Test
 * Author:  Nathan Hanchey
            Dylan Vetter
            Corey Moura
            Connor Inglat
 * Date: May 17th 2022
 ************************************************************/

/* Libraries */
#include <avr/sleep.h> //Contains the methods used to control the sleep modes

/* Function Prototypes */
int command_read(unsigned char data[]);
int command_write(unsigned int pin, unsigned int result, unsigned int test);
int crc_encode(unsigned char data[], unsigned int pin, unsigned int result, unsigned int test);
int crc_decode(unsigned char data[]);
void configure_output(unsigned int pin);
int configure_input(unsigned int pin);
void configure_input_pullup(unsigned int pin);
int configure_analog_input(unsigned int pin);
void configure_sleep_mode(unsigned int sleepmode);
void wakeUp();


/* Facade and Actual Function Pointer Prototypes */
//FACADE&ACTUAL FUNCTION POINTERS
void (*test) (uint8_t, uint8_t);
void (*p_pinMode) (uint8_t, uint8_t);
void (*p_digitalWrite) (uint8_t, uint8_t);
void (*p_analogWrite) (uint8_t, uint8_t);
int (*p_digitalRead) (unsigned char);
int (*p_analogRead) (unsigned char);
//sleep modes pointers?


//SETUP
void setup() {
  
  Serial.begin(115200); //sets the baud rate
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(2, INPUT);   // digital sensor is on digital pin 2

  //FACADE POINTER EXAMPLEs (setup)
  //test = &digitalWrite;
  p_digitalWrite = &digitalWrite;
  p_digitalRead = &digitalRead;
  p_pinMode = &pinMode;
  p_analogRead = &analogRead;
  //+Sleep Modes
}

unsigned char RMSG[3];

// MAIN LOOP
void loop() {

  //FACADE FUNCTION POINTER EXAMPLE (LED)
  //(*test)(13, HIGH);
  //FACADE FUNCTION POINTER EXAMPLE (INPUT)
  //Serial.println((*p_digitalRead)(2));

  if (Serial.available() > 0) {
    //delay(50);
    //Serial.println(Serial.available());

        //Write Test
        command_read(RMSG);
        delay(50); //delay is important

        if(crc_decode(RMSG)){

          //Interpret Instructions

          //Send Back Results
          command_write(RMSG[0], RMSG[1], RMSG[2]);
        }

  }

}


/* Command Read
 *  Input & Output: data[] (encodes unsigned char array)
 *
 */
int command_read(unsigned char data[]) {

   //HAL_UART_Receive(&huart2, data, 3, 10000);
   data[0] = Serial.read();
   delay(5);
   data[1] = Serial.read();
   delay(5);
   data[2] = Serial.read();
   delay(5);

  return 0;
}

/* Serial Comm Commands Write
 * Parameters:
 * pin (unsigned int) -> data byte 0
 * result (unsigned int) -> data byte 1
 * test (unsigned int) -> data byte 2
 */
int command_write(unsigned int pin, unsigned int result, unsigned int test) {

  //Write
  unsigned char data[3];

  crc_encode(data, pin, result, test);

  //HAL_UART_Transmit(&huart2, data, 3, 100);
  Serial.write(data[0]);
  Serial.write(data[1]);
  Serial.write(data[2]);

  return 0;
}

/* CRC Encoding
 * Input & Output: data[] (encodes unsigned char array)
 * Parameters:
 * pin (unsigned int) -> data byte 0
 * result (unsigned int) -> data byte 1
 * test (unsigned int) -> data byte 2
 */
int crc_encode(unsigned char data[], unsigned int pin, unsigned int result, unsigned int test) {

  // Find the data
  unsigned long int crc_packet = (((unsigned long int)pin << 16) & 0xFF0000) + ((result << 8) & 0xFF00) + ((test << 4) & 0xF0);

  // Find
  unsigned int remainder = crc_packet % 5;
  unsigned int crc = 5 - remainder;

  crc_packet += crc;

  data[0] = ((crc_packet >> 16)) & 0xFF;
  data[1] = ((crc_packet >> 8)) & 0xFF;
  data[2] = ((crc_packet) & 0xFF);

  return 0;
}

/* CRC Decoding and Error Checking
 * Input & Output: data[] (decodes unsigned char array)
 * Return Value: 1 indicates correct crc encoding & 0 indicates incorrect encoding
 */
int crc_decode(unsigned char data[]) {

  // Find the data
  unsigned long int crc_packet = (((unsigned long int)data[0] << 16) & 0xFF0000)
      + (((unsigned long int)data[1] << 8) & 0xFF00) + (((unsigned long int)data[2]));

  if(crc_packet % 5) {
    return 0;
  }

  data[2] = (data[2] & 0xF0) >> 4;

  return 1;
}

/*
 * Description: Configures GPIO pin as OUTPUT and turns the output to HIGH. Used for testing GPIO output voltage under load sourcing.
 * Accepts: unsigned int pin - the pin number to configure as OUTPUT
 * Returns: void
 */
void configure_output(unsigned int pin) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, HIGH);
    return;
}






/*
 * Description: Configures GPIO pin as an INPUT. Used for testing input logic levels. The input pin cannot be a pullup,
 * as that would allow the pin to act as a current source and could damage the testing device's DAC.
 * Accepts: unsigned int pin - the pin number to configure as INPUT
 * Returns: int - 0 or 1 depending on input voltage of the pin (LOGIC LOW OR HIGH)
 */
int configure_input(unsigned int pin) {
    pinMode(pin, INPUT);
    return digitalRead(pin);
}

/*
 * Description: Configures GPIO pin as INPUT_PULLUP. Used for testing the pin's unloaded pullup voltage and internal
 * resistance value.
 * Accepts: unsigned int pin - the pin number to configure as INPUT_PULLUP
 * Returns: void
 */
void configure_input_pullup(unsigned int pin) {
    pinMode(pin,INPUT_PULLUP);
    return;
}


/*
 * ADC TEST
 * Description: Returns the analog reading of the selected analog pin (A0, A1, ..., A5). Used for testing the Arduino's
 * ADC.
 * Accepts: unsigned int analogPin - the analog pin number to read
 * Returns: int - 0 to 1023, depending on the voltage reading of the ADC. (0 = GND, 1023 = 5V)
 */
int configure_analog_input(unsigned int analogPin) {
   return analogRead(analogPin); //returns a value 0-1023 (0=GND, 1023 = 5V)
}

/*
 * Description: Configures the Arduino Uno for one of 6 sleep modes. The board is woken with interrupt pin 2 or 3. Used
 * for testing current draw during sleep modes and interrupt pin capability.
 * Accepts: unsigned int sleepmode - the sleep mode for the Arduino to enter (see switch-case)
 *          unsigned int interruptPin - the pin # to configure as an interrupt (Digital 2 or 3 for Arduino)
 * Returns: void
 */
void configure_sleep_mode(unsigned int sleepmode, unsigned int interruptPin) {
    sleep_enable(); //Enables sleep mode
    pinMode(interruptPin, INPUT_PULLUP); //Assign pin 2 or 3 as input pullup
    attachInterrupt(digitalPinToInterrupt(interruptPin), wakeUp, LOW); //set pin 2 or 3 as an interrupt that jumps to wakeUp() when triggered LOW
    switch (sleepmode) { //selects which sleep mode to enter
        case 1:
            set_sleep_mode(SLEEP_MODE_IDLE);
            break;
        case 2:
            set_sleep_mode(SLEEP_MODE_ADC);
            break;
        case 3:
            set_sleep_mode(SLEEP_MODE_PWR_DOWN);
            break;
        case 4:
            set_sleep_mode(SLEEP_MODE_PWR_SAVE);
            break;
        case 5:
            set_sleep_mode(SLEEP_MODE_STANDBY);
            break;
        case 6:
            set_sleep_mode(SLEEP_MODE_EXT_STANDBY);
            break;
        default:
            set_sleep_mode(SLEEP_MODE_IDLE);
            break;
    }
    bitClear(TIMSK0, 0);  //stops the millis() timer so that sleep modes aren't waken by it (SLEEP_MODE_IDLE is woken by the millis() timer)
    sleep_cpu(); //activates the set sleep mode
    //Serial.println("Just woke up!");
    bitSet(TIMSK0, 0); //starts the millis() timer back up
    return;
}

/*
 * Description: ISR used to disable sleep mode and detach the interrupt pin
 * Accepts: void
 * Returns: void
 */
void wakeUp(){
    sleep_disable(); //Disable sleep mode
    detachInterrupt(digitalPinToInterrupt(2)); //remove pin as interrupt
    detachInterrupt(digitalPinToInterrupt(3)); //remove pin as interrupt
    return;
}