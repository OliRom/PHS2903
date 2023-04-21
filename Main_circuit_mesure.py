import time
import Utils as ut
import serial
import numpy as np
import pandas as pd
# import nidaqmx
# from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
# from nidaqmx.constants import (BridgeConfiguration, VoltageUnits,
#                                BridgeUnits, AcquisitionType)
import Parameters as para


def measure_ga():
    start = time.time_ns()  # Starting time
    T = 0  # Initialisation de la tempérautre (valeur peu importante)
    data = list()  # Initialisation de la liste contenant les données

    # Initialisation du contrôleur de puissance
    power_controler = ut.PowerControler(para.daq_ports["power"],30)
    power_controler.set_power(15)

    # Initialisation de la communication sérielle avec le Arduino
    arduino = serial.Serial(ut.get_arduino_port(True), baudrate=9600, timeout=0.2)

    # Charger les coefficients des thermistances
    coef = dict()
    for i in [1, 2]:
        coef[f"thermi_{i}"] = np.load(para.coef_file_paths[f"thermi_{i}"])["coef"]

    power_controler.set_power(10)
    power_controler.start_pwm()
    print("Temps - T1 - T2 - Tmoyen - Puissance")
    counter = 0

    while T <= para.T_max + para.T_0 + 5:
        v1, v2 = ut.mesure_v(para.daq_ports["thermi_1"]), ut.mesure_v(para.daq_ports["thermi_2"])
        T1, T2 = ut.v_to_temp(v1, *coef["thermi_1"]), ut.v_to_temp(v2, *coef["thermi_2"])
        temps = time.time_ns() - start

        T = (T1 + T2) / 2
        p = power_controler.power

        data.append((temps/1e9, T1, T2, T, p))

        # Envoyer la température moyenne au Arduino
        if counter % 5 == 1:
            arduino.write(bytes(str(T2-para.T_0), "utf-8"))

        print("\r", end="")
        #print(data[-1]-np.array([0, para.T_0, para.T_0, para.T_0, 0]), end="")
        print(f"{round(T1-para.T_0, 2)} - {round(T2-para.T_0, 2)}", end="")
        counter += 1

        time.sleep(0.1)

    power_controler.stop_pwm()

    # Enregistrement des données
    df = pd.DataFrame(data, columns=["t", "T1", "T2", "T", "p"])
    df.to_csv(para.meas_file_paths["data"])

    # Calculer l'enthalpie de fusion avec toutes les température moyenne et la puissance
    'enthalpie = Calculer_enthalpie(Tmoyen,P,t)'

    # Calculer la capacité thermique
    'capacité = Calculer_capacité(Tmoyen,P,t)'

    # Afficher la courbe de température en fonction du temps
    'plot_data()'


if __name__ == "__main__":
    measure_ga()
