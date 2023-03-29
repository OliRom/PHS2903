// Valeur des constantes du PID à 25C (min) et 40C (max)
// proportional constant
#define kp_min 20
#define kp_max 40
// integral constant
#define ki_min 1
#define ki_max 1.5
// derivative constant
#define kd_min 15
#define kd_max 15
// temperature constant
#define kt_min 25
#define kt_max 25

#define thermo_pin 10
#define power_pin 9

// Coefficients de la thermistance
#define e 15
#define r 115000
#define a 0.00113
#define b 0.000235
#define c 8.57e-8

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

float kp(float T){return kp_min + (kp_max-kp_min)/15 * (T-25);}
float ki(float T){return ki_min + (ki_max-ki_min)/15 * (T-25);}
float kd(float T){return kd_min + (kd_max-kd_min)/15 * (T-25);}
float kt(float T){return kt_min + (kt_max-kt_min)/15 * (T-25);}

float compute_power(float T, float *error) {
  float integral = 0;
  for (int i=0; i<nb_error; i++){integral += error[i];}
  
  return kp(T) * error[0] + ki(T) * integral + kd(T) * (error[0]-error[1]) + constrain((T-30)/10 * kt(T), 0, 100);
}

float v_to_temp(float v) {
  float arg = r * v / (e-v);
  float denom = a + b * log(arg) + c * pow(log(arg), 3);
  return 1 / denom;
}

void set_power(float power) {
  power = constrain(power, 0, 255);
  
  analogWrite(power_pin, power);
  // Serial.print("Pow:");
  // Serial.println(power);
}

void setup() {
  pinMode(thermo_pin, INPUT);
  pinMode(power_pin, OUTPUT);
  
  Serial.begin(9600);
  delay(5000);
  while (Serial.available() == 0) {}
  cible = Serial.readString().toFloat();
  // Serial.println("Pret a commencer!");
}

void loop() {
  temp_v = float(analogRead(thermo_pin)) / 1024 * 5;
  temp = v_to_temp(temp_v) - 273.15;
  rotate(error, cible-temp);

  power = compute_power(temp, error);
  set_power(power);
  
//  Serial.print("V:");
//  Serial.print(temp_v);
//  Serial.print("  Temp:");
//  Serial.print(temp);
//  Serial.print("  ");

  delay(500);

  if (Serial.available()) {cible = Serial.readString().toFloat();}
}
