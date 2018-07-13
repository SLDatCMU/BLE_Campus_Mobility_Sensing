/*
 Circuit:
 mcp3002 sensor attached to pins 10 - 13:
 CS: pin 10
 MOSI: pin 11
 MISO: pin 12
 SCK: pin 13
 */

const byte READ = 0b00011010;     // MCP3002's read command
// This will cause it to use channel 0 in single-channel mode, and the 
// returned data will be MSB-first.

// Assignments to external pins for SPI interface:
const int chipSelect = 10;
const int serialClock = 13;
const int pMOSI = 11;
const int pMISO = 12;

const float VREF_LSB = 4.07/1024;

void setup() {
  Serial.begin(9600);

  // initalize the  data ready and chip select pins:
  pinMode(chipSelect, OUTPUT);
  pinMode(serialClock, OUTPUT);
  pinMode(pMOSI, OUTPUT);
  pinMode(pMISO, INPUT);

  // Chip select must be set high at some point after power-on to 
  // ensure correct operation of ADC.
  digitalWrite(chipSelect, HIGH);

  // give the sensor time to set up:
  delay(100);
}

void loop() {
  // Start by setting the clock high and chip-select low:
  digitalWrite(serialClock, HIGH);
  digitalWrite(chipSelect, LOW);
  
  // Now write the read command, which is the configuration:
  byte temp_cmd = READ;
  for (int i = 0; i < 8; i++)
  {
    digitalWrite(pMOSI, temp_cmd & 0x80);

    // Toggle clock low, then high to register command bit with ADC:
    digitalWrite(serialClock, LOW);
    digitalWrite(serialClock, HIGH);

     // Shift the temp command left to get the next bit:
     temp_cmd <<= 1;
  }
  
  // Now that the command has been written, each clock falling edge will 
  // cause the ADC to output a bit. First output bit was null (low) and 
  // should have been taken care of by the last falling edge in the 
  // command byte sequence. 
  // The next 10 bits out will be the relevant data bits: 
  unsigned short tmp_dat_MSB = 0;
  unsigned short tmp_dat_LSB = 0;
  unsigned short tmp_dat_other = 0;
  
  // Read data in MSB format:
  for (int i = 0; i < 10; i++)
  {
    // Data is output on the clock falling edge:
    digitalWrite(serialClock, LOW);
    digitalWrite(serialClock, HIGH);
    tmp_dat_MSB <<= 1;
    tmp_dat_MSB |= ( 0x01 & digitalRead(pMISO) );
//    Serial.println( tmp_dat_MSB & 0x1 );
  }

  // Read data in LSB format.
  // Note that the 0 bit is not repeated between MSB and LSB transmissions!
  tmp_dat_LSB |= (0x01 & tmp_dat_MSB);
  for (int i = 1; i < 10; i++)
  {
    // Data is output on the clock falling edge:
    digitalWrite(serialClock, LOW);
    digitalWrite(serialClock, HIGH);
//    tmp_dat_LSB <<= 1;
    tmp_dat_LSB |= ( digitalRead(pMISO) << i );
  }

  // Read 10 more bits to make sure they are all 0s.
  for (int i = 0; i < 10; i++)
  {
    // Data is output on the clock falling edge:
    digitalWrite(serialClock, LOW);
    digitalWrite(serialClock, HIGH);
//    tmp_dat_other <<= 1;
    tmp_dat_other |= ( digitalRead(pMISO) << i );
  }
  
  // End the transaction by writing chipSelect high:
  digitalWrite(chipSelect, HIGH);
  digitalWrite(serialClock, LOW);
  Serial.println("Done reading!");
  float val = VREF_LSB * tmp_dat_MSB;
  Serial.print(tmp_dat_MSB, BIN);
  Serial.print(" ");
  Serial.println(val);

  val = VREF_LSB * tmp_dat_LSB;
  Serial.print(tmp_dat_LSB, BIN);
  Serial.print(" ");
  Serial.println(val);
  
  Serial.println(tmp_dat_other, BIN);
  Serial.println("Done printing.");
}

