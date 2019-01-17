byte ibyte = B00000000;
byte ibyte2 = B11111111;
byte mask = B00000000;
int i,j;
int pins[] = {36, 34, 32, 30, 37, 35, 33, 31};
int pins2[] = {46, 44, 42, 40, 47, 45, 43, 41};
byte incoming;

void setup() 
{                
  Serial.begin(9600);
  for(i=0;i<8;i++){
    pinMode(30+i,OUTPUT);
    pinMode(40+i,OUTPUT);
  }
}

void loop() {
  mask = B10000000;
  for(i=0; i<=7; i++){
    digitalWrite(pins[i], HIGH && (ibyte & mask));
    digitalWrite(pins2[i], HIGH && (ibyte2 & mask));
    mask = mask >> 1;
    if(ibyte == B11111111){
      ibyte = B00000000;
    }
  }
  ibyte = ibyte + 1;
  ibyte2 = 255 - ibyte;
  Serial.print("\nABCDEFGH : ");
  print_byte(ibyte);
  delay(500); 
}

void print_byte(byte val)
{
    byte i;
    for(byte i=0; i<=7; i++)
    {
      Serial.print(val >> i & 1, BIN);
    }
}
