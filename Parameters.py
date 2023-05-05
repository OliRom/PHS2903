import os
import numpy as np


data_path = os.path.join("data")

etalon_path = os.path.join(data_path, "etalonnage_v_t")
etal_data_file_paths = {
    "thermi_1": os.path.join(etalon_path, "thermi_1.csv"),
    "thermi_2": os.path.join(etalon_path, "thermi_2.csv"),
    "thermi_ext": os.path.join(etalon_path, "thermi_ext.csv"),
}

coef_path = os.path.join(data_path, "coefficients")
coef_file_paths = {
    "thermi_1": os.path.join(coef_path, "thermi_1.npz"),
    "thermi_2": os.path.join(coef_path, "thermi_2.npz"),
    "thermi_ext": os.path.join(coef_path, "thermi_ext.npz"),
}

meas_path = os.path.join(data_path, "measurement")
meas_file_paths = {
    "data": os.path.join(meas_path, "data.csv"),
    "results": os.path.join(meas_path, "results.npz"),
}

daq_ports = {
    "thermi_1": "myDAQ1/ai0",
    "thermi_2": "myDAQ1/ai1",
    "power": "myDAQ1/ao0",
    "thermi_ext": "mydaq1/ai0",
}

coef_init_guess = [
    0.00113,  # a
    0.000235,  # b
    8.57e-8,  # c
    15,  # e
    115e3,  # r
]

T_max = 40  # Température maximale
T_0 = 273.15  # Température en Kelvin

m_recipient = 36.3755  # Masse du récipient vide
m_totale = 83.6396  # Massedu récipient avec le Gallium
m_Ga = m_totale - m_recipient  # Masse du gallium
a_m=0.0001/(6**0.5) #incertitude sur la masse

c_etalon = 30.0542743832689 #capacité thermique du récipient + eau (moyenne étalonnage)
m_eau = 7.1141 #masse d'eau en g
c_eau = (4.1818+4.1785)/2 #capacité thermique massique de l'eau [J/(g K)]
a_c_eau = (4.1818-4.1785)/2 #inceritude sur c_eau. 4.1818 à 20C, 4.1785 à 40C
c_recipient = c_etalon-c_eau*m_eau  # Capacité thermique massique du récipient [J/K]
a_c_etalon = 0.348360681674184   #Incertitude type A sur la capacité thermique du récipient + eau (étalonnage)
a_c_recipient = (a_c_etalon**2+(m_eau*a_c_eau)**2+(c_eau*0.0001)**2/12)**0.5

p_max = 30 #Watt max élément chauffant du Ga
p_min = 1 #Watt min élément chauffant Ga (courant de fuite)
R= 18.0907 #Ohm résistance élément chauffant
a_R=0.01846401149396240000
  #Incertitude résistance élément chauffant appareil Yves
v_max=18  #V quand p_max
a_Vmx=0.0001*v_max+0.003 #incertitude voltage max élément chauffant (résolution Gwinstek GPS-1850 D)
a_PWM=12**(-0.5)/16e6 #incertitude sur la période du PWM, fréquence du processeur: 16MHz.
Q=0.0452 #voir présentation orale. Pertes de chaleur.

def a_p(P): #incertitude sur P en fonction de P
    return ((2*P*a_Vmx/v_max)**2+25*(P**2+(v_max**2/R)**2)*a_PWM+(P*a_R/R)**2+Q**2)**0.5

#coef étalonné thermi 1:
A_1=1.71097855e-03
B_1=7.33832636e-05
C_1=4.73429921e-07
E_1=1.33374599e+03
R_1=1.48383888e+08

stdev_th1=0.04942304589048282 #écart type de la courbe d'étalonnage
def dT_dV_th1(T1): #dérivée de la courbe d'étalonnage de thermi 1
    x=(A_1-1/T1)/C_1
    y=((B_1/(3*C_1))**3+x**2/4)**0.5
    arg=np.exp((y-x/2)**(1/3)-(y+x/2)**(1/3))

    dV_darg=E_1*R_1/(R_1+arg)**2

    darg_dx=-arg*((y-x/2)**(-2/3)+(y+x/2)**(-2/3))/6
    darg_dy=arg*((y-x/2)**(-2/3)-(y+x/2)**(-2/3))/3
    dy_dx=x/(4*y)
    dx_dT=1/(C_1*T1**2)
    darg_dT=(darg_dx+darg_dy*dy_dx)*dx_dT

    dV_dT=dV_darg*darg_dT
    return 1/dV_dT
def a_T_th1(T1): #incertitude sur la T de thermi 1
    return (stdev_th1**2+3.0976e-12*dT_dV_th2(T1)**2+0.01)**0.5

#coef étalonné thermi 2:
A_2=1.71097855e-03
B_2=7.33832636e-05
C_2=4.73429921e-07
E_2=1.33374599e+03
R_2=1.48383888e+08

R = 19.026667  # Ohm résistance élément chauffant
p_max = 18**2/R  # Watt max élément chauffant du Ga
# a_R =  # Incertitude résistance
# a_V= incertitude voltage élément chauffant

stdev_th2=0.04942304589048282 #écart type de la courbe d'étalonnage de thermi 2
def dT_dV_th2(T2): #dérivée de la courbe d'étalonnage de thermi 2 (steinhart-hart inverse)
    x=(A_2-1/T2)/C_2
    y=((B_2/(3*C_2))**3+x**2/4)**0.5
    arg=np.exp((y-x/2)**(1/3)-(y+x/2)**(1/3))

    dV_darg=E_2*R_2/(R_2+arg)**2

    darg_dx=-arg*((y-x/2)**(-2/3)+(y+x/2)**(-2/3))/6
    darg_dy=arg*((y-x/2)**(-2/3)-(y+x/2)**(-2/3))/3
    dy_dx=x/(4*y)
    dx_dT=1/(C_2*T2**2)
    darg_dT=(darg_dx+darg_dy*dy_dx)*dx_dT

    dV_dT=dV_darg*darg_dT
    return 1/dV_dT
def a_T_th2(T2): #incertitude sur la T de thermi 2
    return (stdev_th2**2+3.0976e-12*dT_dV_th2(T2)**2+0.01)**0.5

def a_T(T1,T2): #incertitude sur la T moyenne de thermi 2 et thermi 1
    return 0.5*(a_T_th1(T1)**2+a_T_th2(T2)**2)**0.5

