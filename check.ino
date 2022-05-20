int s1=A0;
int s2=A1;
int s3=A2;
int s4=A3;//신호 값 사용 범위




void setup() {
  Serial.begin(9600);
  
  

}

void loop() {
  int val1=analogRead(s1);
  int val2=analogRead(s2);
  int val3=analogRead(s3);
  int val4=analogRead(s4);// 신호 받기
  Serial.print(val1);
  Serial.print(' ');
  Serial.print(val2);
  Serial.print(' ');
  Serial.print(val3);
  Serial.print(' ');
  Serial.println(val4);
  delay(500);
  

}
