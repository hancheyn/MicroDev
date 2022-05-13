
/************************************************************
 * Description: Serial Communication to Raspi Test
 * Author:  Nathan Hanchey
            Dylan Vetter
 * Date: May 13th 2022
 ************************************************************/

// Function Prototypes
// Read and Write I/O
int command_read(unsigned char data[]);
int command_write(unsigned int pin, unsigned int result, unsigned int test);
int crc_encode(unsigned char data[], unsigned int pin, unsigned int result, unsigned int test);
int crc_decode(unsigned char data[]);


void setup() {
  
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(2, INPUT);   // digital sensor is on digital pin 2 
 
}

unsigned char RMSG[3];

void loop() {
  // 
  
  if (Serial.available() > 0) {
    //delay(50);
    //Serial.println(Serial.available());   
        
        //inByte = Serial.read();
        //delay(50);
        //Serial.write(inByte);
     
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
