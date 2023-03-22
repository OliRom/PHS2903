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
    power_controler = ut.PowerControler(para.daq_ports["power"])
    power_controler.set_power(15)

    # Initialisation de la communication sérielle avec le Arduino
    arduino = serial.Serial(ut.get_arduino_port(), baudrate=9600, timeout=0.2)

    # Charger les coefficients des thermistances
    coef = dict()
    for i in [1, 2]:
        coef[f"thermi_{i}"] = np.load(para.coef_file_paths[f"thermi_{i}"])["coef"]

    while T <= para.T_max:
        v1, v2 = ut.mesure_voltage(para.daq_ports["thermi_1"]), ut.measure_v(para.daq_ports["thermi_2"])
        T1, T2 = ut.v_to_temp(V1, *coef["thermi_1"]), ut.v_to_temp(V2, *coef["thermi_2"])
        t = time.time_ns() - start

        T = (T1+T2)/2
        P = power_controler.power

        data.append((t, T1, T2, T, P))

        # Envoyer la température moyenne au Arduino
        arduino.write(bytes(T, "utf-8"))

        time.sleep(0.1)

    # Enregistrement des données
    df = pd.DataFrame(data, columns=["t", "T1", "T2", "T", "P"])
    df.to_csv(para.meas_file_paths["data"])

    # Calculer l'enthalpie de fusion avec toutes les température moyenne et la puissance
    'enthalpie = Calculer_enthalpie(Tmoyen,P,t)'

    # Calculer la capacité thermique
    'capacité = Calculer_capacité(Tmoyen,P,t)'

    # Afficher la courbe de température en fonction du temps
    'plot_data()'


if __name__ == "__main__":
    measure_ga()
