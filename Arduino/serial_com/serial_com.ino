/************************************************************
 * Description: Serial Communication to Raspi Test
 * Author:  Nathan Hanchey
            Dylan Vetter
            Corey Moura
            Connor Inglat
 * Date: May 17th 2022
 ************************************************************/

// Function Prototypes
// Read and Write I/O
int command_read(unsigned char data[]);
int command_write(unsigned int pin, unsigned int result, unsigned int test);
int crc_encode(unsigned char data[], unsigned int pin, unsigned int result, unsigned int test);
int crc_decode(unsigned char data[]);
int configure_output(unsigned int pin);
int configure_input(unsigned int pin);
int configure_input_pullup(unsigned int pin);
int configure_analog_input(unsigned int pin);
int configure_sleep_mode(unsigned int sleepmode);

void setup() {
  
  Serial.begin(115200); //sets the baud rate
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(2, INPUT);   // digital sensor is on digital pin 2 
 
}

unsigned char RMSG[3];

void loop() {
  // 
  
  if (Serial.available() > 0) { //Serial.available() returns the number of bytes read
    //delay(50);
    //Serial.println(Serial.available());   
        
        //inByte = Serial.read(); //Serial.read() returns the first available byte in the serial buffer, then removes it.
        //delay(50);
        //Serial.write(inByte); //Serial.write(x) writes binary data to the serial port as a byte or series of bytes
     
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
Configures GPIO pin as OUTPUT and turns the output to HIGH
*/
int configure_output(unsigned int pin) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, HIGH);

    return 0;
}

/*
Configures GPIO pin as an INPUT
Returns HIGH or LOW depending on input voltage
*/
int configure_input(unsigned int pin) {
    pinMode(pin, INPUT);
    delay(50);
    return digitalRead(pin);
}

/*
Configures GPIO pin as INPUT_PULLUP
*/
int configure_input_pullup(unsigned int pin) {
    pinMode(pin,INPUT_PULLUP);

    return 0;
}


/*
Returns the analog reading on the pin
*/
int configure_analog_input(unsigned int analogPin) {
   return analogRead(analogPin);
}

int configure_sleep_mode(unsigned int sleepmode) {

    return 0;
}