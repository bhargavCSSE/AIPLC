const int data_pin = 11; 
const int shld_pin = 8; 
const int clk_pin = 12; 
const int ce_pin = 9;
byte ibyte = B00000000;
byte mask = B00000000;
int i;
int pins[] = {36, 34, 32, 30, 37, 35, 33, 31};
byte incoming;

void setup() 
{                
  Serial.begin(9600);
  pinMode(30,OUTPUT);
  pinMode(31,OUTPUT);
  pinMode(32,OUTPUT);
  pinMode(33,OUTPUT);
  pinMode(34,OUTPUT);
  pinMode(35,OUTPUT);
  pinMode(36,OUTPUT);
  pinMode(37,OUTPUT);
  
  pinMode(shld_pin, OUTPUT);
  pinMode(ce_pin, OUTPUT);
  pinMode(clk_pin, OUTPUT);
  pinMode(data_pin, INPUT);

  digitalWrite(clk_pin, HIGH);
  digitalWrite(shld_pin, HIGH);

}

void loop() {
  mask = B10000000;
  for(i=0; i<=7; i++){
    digitalWrite(pins[i], HIGH && (ibyte & mask));
    mask = mask >> 1;
    if(ibyte == B11111111){
      ibyte = B00000000;
      Serial.print("\n\nBinary value will be reset to 00000000\n");
      delay(2000);
    }
  }
  ibyte = ibyte + 1;
  incoming = read_shift_regs();
  Serial.print("\nABCDEFGH : ");
  print_byte(incoming);
  delay(50); 
}

byte read_shift_regs()
{
  byte the_shifted = 0;  
  digitalWrite(shld_pin, LOW);
  delayMicroseconds(5);
  digitalWrite(shld_pin, HIGH);
  delayMicroseconds(5);

  pinMode(clk_pin, OUTPUT);
  pinMode(data_pin, INPUT);
  digitalWrite(clk_pin, HIGH);
  digitalWrite(ce_pin, LOW);

  the_shifted = shiftIn(data_pin, clk_pin, MSBFIRST);
  digitalWrite(ce_pin, HIGH);

  return the_shifted;
}

void print_byte(byte val)
{
    byte i;
    for(byte i=0; i<=7; i++)
    {
      Serial.print(val >> i & 1, BIN);
    }
}

