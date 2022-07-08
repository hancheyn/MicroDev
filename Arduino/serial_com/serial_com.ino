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
void command_read(unsigned char data[]);
void command_write(unsigned int pin, unsigned int result, unsigned int test);
void crc_encode(unsigned char data[], unsigned int pin, unsigned int result, unsigned int test);
int crc_decode(unsigned char data[]);

/* Config Function Prototypes */
void configure_output(unsigned int pin, unsigned int logic);
int configure_input(unsigned int pin);
void configure_input_pullup(unsigned int pin);
int configure_analog_input(unsigned int pin);
void configure_sleep_mode(unsigned int sleepmode, unsigned int interruptPin);
void wakeUp();

struct pin pin_set(uint32_t pin, uint8_t pin_id);
void init_pins(struct pin pins[]);

/* Facade and Actual Function Pointer Prototypes */
void (*test) (uint8_t, uint8_t);
void (*p_pinMode) (uint8_t, uint8_t);
void (*p_digitalWrite) (uint8_t, uint8_t);
void (*p_analogWrite) (uint8_t, uint8_t);
int (*p_digitalRead) (unsigned char);
int (*p_analogRead) (unsigned char);
// sleep modes pointers?


/* Pin Struct */
struct pin {
  uint32_t pin;
  uint8_t pin_id;
};

/* Global Variables */
unsigned char RMSG[3];
unsigned int test_result;
struct pin PINS_[64];

/* Runs once upon startup of the program */
void setup() {

    Serial.begin(115200); //sets the baud rate
    while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB port only
    }

    //FACADE POINTER EXAMPLES (setup)
    //test = &digitalWrite;
    p_digitalWrite = &digitalWrite;
    p_digitalRead = &digitalRead;
    p_pinMode = &pinMode;
    p_analogRead = &analogRead;
    //+Sleep Modes

    init_pins(PINS_);
}


/* Runs repeatedly after setup has completed */
void loop() {

    if (Serial.available() > 0) { //Serial.available() returns the number of bytes read
        delay(50); //NEEDED
        
        //Write Test
        command_read(RMSG);

        if(crc_decode(RMSG)){
            //Interpret Instructions
            //RMSG[0] = pin under test, RMSG[1] = Special Instructions, RMSG[2] = Test Identification
            unsigned int pin_val = PINS_[RMSG[0]].pin;
            switch (RMSG[2]) { // Test Identification #
                case 1: 
                    configure_output(pin_val, RMSG[1]);
                    command_write(RMSG[0], RMSG[1], RMSG[2]);
                    break;
                case 2:
                    configure_output(pin_val, RMSG[1]);
                    command_write(RMSG[0], RMSG[1], RMSG[2]);
                    break;
                case 3:
                    configure_input_pullup(pin_val);
                    command_write(RMSG[0], RMSG[1], RMSG[2]);
                    break;
                case 4:
                    // configure pull down (does not exist for arduino)
                    command_write(RMSG[0], RMSG[1], RMSG[2]);
                    break;
                case 5:
                    test_result = configure_input(pin_val);
                    command_write(RMSG[0], test_result, RMSG[2]);
                    break;
                case 6:
                    test_result = configure_analog_input(pin_val);
                    command_write(RMSG[0], test_result, RMSG[2]);
                    break;
                case 7:
                    configure_sleep_mode(RMSG[1], RMSG[0]); //send sleepmode & pin#
                    //command_write(RMSG[0], RMSG[1], RMSG[2]);
                    break;
                default:
                    command_write(RMSG[0], RMSG[1], RMSG[2]);
                    break;
            }
            //Send Back Results
            //command_write(RMSG[0], RMSG[1], RMSG[2]);
        }
        else {
          command_write(RMSG[0], RMSG[1], RMSG[2]);
        }
    }

}

/*
 * Description: Reads the next three bytes from the serial communication port and stores them into the data array
 * Accepts: unsigned char data[] - the data array used to store the read data
 * Returns: void
 */
void command_read(unsigned char data[]) {
    //HAL_UART_Receive(&huart2, data, 3, 10000);
    data[0] = Serial.read(); //Serial.read() returns the first available byte in the serial buffer, then removes it.
    data[1] = Serial.read();
    data[2] = Serial.read();

    return;
}

/*
 * Description: Calls the crc_encode function then writes the resulting encoded bytes to the serial communication port
 * Accepts: unsigned int pin - the pin number to encode and send
 *          unsigned int result - the result of the test to encode and send
 *          unsigned int test - the test number to encode and send
 * Returns: void
 */
void command_write(unsigned int pin, unsigned int result, unsigned int test) {

    //Write
    unsigned char data[3];

    crc_encode(data, pin, result, test);

    //HAL_UART_Transmit(&huart2, data, 3, 100);
    Serial.write(data[0]); //Serial.write(x) writes binary data to the serial port as a byte or series of bytes
    Serial.write(data[1]);
    Serial.write(data[2]);

    return;
}

/*
 * Description: Encodes a crc packet with pin #, test, and result. Stores those three bytes into data[]
 * Accepts: unsigned char data[] - the data array where the encoded message is written to
 *          unsigned int pin - the pin number to encode
 *          unsigned int result - the result of the test to encode
 *          unsigned int test - the test number to encode
 * Returns: void
 */
void crc_encode(unsigned char data[], unsigned int pin, unsigned int result, unsigned int test) {

    // Find the data
    unsigned long int crc_packet = (((unsigned long int)pin << 16) & 0xFF0000) + ((result << 8) & 0xFF00) + ((test << 4) & 0xF0);

    // Find
    unsigned int remainder = crc_packet % 5;
    unsigned int crc = 5 - remainder;

    crc_packet += crc;

    data[0] = ((crc_packet >> 16)) & 0xFF;
    data[1] = ((crc_packet >> 8)) & 0xFF;
    data[2] = ((crc_packet) & 0xFF);

    return;
}

/*
 * Description: CRC Decoding and Error Checking
 * Accepts: unsigned char data[] - the data array to decode
 * Returns: int - 0 if the data size is wrong, 1 otherwise
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
 *          unsigned int logic - HIGH or LOW logic
 * Returns: void
 */
void configure_output(unsigned int pin, unsigned int logic) {
    pinMode(pin, OUTPUT);
    if(logic) {
      digitalWrite(pin, HIGH);
    }
    else {
      digitalWrite(pin, LOW);
    }
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
 * Description: Returns the analog reading of the selected analog pin (A0, A1, ..., A5). Used for testing the Arduino's
 * ADC.
 * Accepts: unsigned int analogPin - the analog pin number to read
 * Returns: int - 0 to 1023, depending on the voltage reading of the ADC. (0 = GND, 1023 = 5V)
 */
int configure_analog_input(unsigned int analogPin) {
   return (analogRead(analogPin) >> 2); //returns a value 0-1023 (0=GND, 1023 = 5V)
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


/*
 * Description: Builds Struct for Pins
 * Accepts: uint32_t - pin value for board
 *          uint8_t - pin value from pi
 * Returns: pin Struct
 */
struct pin pin_set(uint32_t pin, uint8_t pin_id) {

  struct pin P;
  P.pin = pin;
  P.pin_id = pin_id;

  return P;
}


/*
 * Description: Initializes Struct Array for Pins
 * Accepts: pin struct array- pin struct array of pin values
 * Returns: pin Struct array (through pointer)
 */
 //Initialize pin struct array
void init_pins(struct pin pins[]) {

 //Pin 0 Example | PA5
  pins[0] = pin_set(13,  23);

  //Pin 1 | NA
  pins[1] = pin_set(0x00,  1);

  //Pin 2 | NA
  pins[2] = pin_set(0x0C,  2);

  //Pin 3 | NA
  pins[3] = pin_set(0x00,  3);

  //Pin 4 | NA
  pins[4] = pin_set(0x00,  4);

  //Pin 5 | SCL I2C
  pins[5] = pin_set(15,  5);

  //Pin 6 | NA
  pins[6] = pin_set(0x06,  6);

  //Pin 7 | NA
  pins[7] = pin_set(0x09,  7);

  //Pin 8 | NA
  pins[8] = pin_set(0x08,  8);

  //Pin 9 | REF
  pins[9] = pin_set(0x00,  9);

  //Pin 10 | NA
  pins[10] = pin_set(0x00, 10);

  //Pin 11 | E5V
  pins[11] = pin_set(0x00, 11);

  //Pin 12 | VDD
  pins[12] = pin_set(0x00, 12);

  //Pin 13 | AVDD
  pins[13] = pin_set(0x00, 13);

  //Pin 14 | NA
  pins[14] = pin_set(0x00, 14);

  //Pin 15 | SDA I2C
  pins[15] = pin_set(14, 15);

  //Pin 16 | NA
  pins[16] = pin_set(0x05, 16);

  //Pin 17 | NA
  pins[17] = pin_set(0x0E, 17);

  //Pin 18 | 3V3
  pins[18] = pin_set(0x00, 18);

  //Pin 19 | NA
  pins[19] = pin_set(0x0D, 19);

  //Pin 20 | RESET
  pins[20] = pin_set(0x00, 20);

  //Pin 21 | D12
  pins[21] = pin_set(12, 21);

  //Pin 22 | NA
  pins[22] = pin_set(0x0B, 22);

  //Pin 23 | D13
  pins[23] = pin_set(13, 23);

  //Pin 24 | NA
  pins[24] = pin_set(0x0C, 24);

  //Pin 25 | NA
  pins[25] = pin_set(0x0D, 25);

  //Pin 26 | NA
  pins[26] = pin_set(0x07, 26);

  //Pin 27 | NA
  pins[27] = pin_set(0x0F, 27);

  //Pin 28 | 5V
  pins[28] = pin_set(0x00, 28);

  //Pin 29 | NA
  pins[29] = pin_set(0x02, 29);

  //Pin 30 | D10
  pins[30] = pin_set(10, 30);

  //Pin 31 | NA
  pins[31] = pin_set(0x0C, 31);

  //Pin 32 | D11
  pins[32] = pin_set(11, 32);

  //Pin 33 | NA
  pins[33] = pin_set(0x0F, 33);

  //Pin 34 | A0 & D14
  pins[34] = pin_set(A0, 34);

  //Pin 35 | NA
  pins[35] = pin_set(0x0E, 35);

  //Pin 36 | VIN
  pins[36] = pin_set(0x00, 36);

  //Pin 37 | D7
  pins[37] = pin_set(7, 37);

  //Pin 38 | NA
  pins[38] = pin_set(0x01, 38);

  //Pin 39 | D8
  pins[39] = pin_set(8, 39);


  //Pin 40 | D9
  pins[40] = pin_set(9, 40);

  //Pin 41 | NA
  pins[41] = pin_set(0x00, 41);

  //Pin 42 | A2
  pins[42] = pin_set(A2, 42);

  //Pin 43 | NA
  pins[43] = pin_set(0x00, 43);

  //Pin 44 | A1 & D15
  pins[44] = pin_set(A1, 44);

  //Pin 45 | D5
  pins[45] = pin_set(5, 45);

  //Pin 46 | NA
  pins[46] = pin_set(0x0E, 46);

  //Pin 47 | D6
  pins[47] = pin_set(6, 47);

  //Pin 48 | NA
  pins[48] = pin_set(0x0F, 48);

  //Pin 49 | NA
  pins[49] = pin_set(0x02, 49);

  //Pin 50 | A4
  pins[50] = pin_set(A4, 50);

  //Pin 51 | VBAT
  pins[51] = pin_set(0x00, 51);

  //Pin 52 | A3
  pins[52] = pin_set(A3, 52);

  //Pin 53 | D3
  pins[53] = pin_set(3, 53);

  //Pin 54 | AGND
  pins[54] = pin_set(0x00, 54);

  //Pin 55 | D4
  pins[55] = pin_set(4, 55);

  //Pin 56 | NA
  pins[56] = pin_set(0x0D, 56);

  //Pin 57 | NA
  pins[57] = pin_set(0x03, 57);

  //Pin 58 | A5
  pins[58] = pin_set(A5, 58);

  //Pin 59 | D0
  pins[59] = pin_set(0, 59);

  //Pin 60 | D1
  pins[60] = pin_set(1, 60);

  //Pin 61 | D2
  pins[61] = pin_set(2, 61);

  //Pin 62 | NA
  pins[62] = pin_set(0x04, 62);

}
