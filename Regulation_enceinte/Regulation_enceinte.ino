#define kp 1  // proportional constant
#define ki 1  // integral constant
#define kd 1  // derivative constant

#define thermo_pin 10
#define power_pin 9

#define nb_error 10  // Nombre de valeurs d'erreur à garder pour calculer le PID
int t;
float error[nb_error] = {0};
float temp_v;
float temp;
float cible;
float power;

void rotate(float *arr, float new_element=0) {
  for (int i=nb_error-1; i>=1; i--) {arr[i] = arr[i-1];}
  arr[0] = new_element;
}

float compute_power(float *error) {
  float integral = 0;
  for (int i=0; i<nb_error; i++){integral += error[i];}
  
  return kp*error[0] + ki*integral + kd * (error[0]-error[1]);
}

float v_to_temp(float v) {
  return 0;
}

void set_power(float power) {
  if (power<0) {power=0;}
  else if (power<255) {power=255;}
  
  analogWrite(power_pin, power);
  Serial.println(power);
}

void setup() {
  pinMode(thermo_pin, INPUT);
  pinMode(power_pin, OUTPUT);
  
  Serial.begin(9600);
  delay(5000);
  while (Serial.available() == 0) {}
  cible = Serial.readString().toFloat();
  Serial.println("Pret a commencer!");
}

//void loop() {
//  digitalWrite(10, HIGH);
//  while (Serial.available() == 0){
//    delay(100);
//  }
//  
//  digitalWrite(10, LOW);
//  t = Serial.readString().toInt();
//
//  digitalWrite(9, HIGH);
//  if (t > 4){
//    digitalWrite(9, HIGH);
//    Serial.print(t);
//  }
//  else {
//    digitalWrite(9, LOW);
//    Serial.print(t);
//  }
//  delay(100);
//}

void loop() {
  temp_v = analogRead(thermo_pin);
  temp = v_to_temp(temp_v);
  rotate(error, cible-temp);

  power = compute_power(error);
  set_power(power);

  delay(1000);
  
//  for (int i=0; i<nb_error; i++) {
//    Serial.print(error[i]);
//    Serial.print(' ');
//  }
//  Serial.println();
//  delay(1000);

  if (Serial.available()) {cible = Serial.readString().toFloat();}
}
