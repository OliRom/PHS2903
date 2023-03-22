import serial
import serial.tools.list_ports as list_ports
import numpy as np
import math as mt
import time
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader, AnalogMultiChannelReader
from nidaqmx.constants import (ResolutionType, VoltageUnits, BridgeUnits, AcquisitionType)
import Parameters as para


def get_arduino_port():
    ports = list_ports.comports()
    ports = [(port, desc) for port, desc, _ in sorted(ports) if "Arduino" in desc]

    assert len(ports) != 0, "Aucun port n'a été reconnu comme étant connecté à un Arduino"

    if len(ports) > 1:
        print("Voici les Arduinos connectés aux ports:")
        for i, (port, desc) in enumerate(ports):
            print(f"{i+1} - {port}: {desc}")
        num = int(input("\nVeuillez sélectionner le numéro du port à connecter: "))

        return ports[num-1][0]

    return ports[0][0]


def v_to_temp(v, a, b, c, e, r):
    '''Fonction qui converti une valeur de tension en une valeur de température pour une thermistance'''
    arg = r * v / (e-v)
    denom = a + b * np.log(arg) + c * (np.log(arg))**3
    return 1 / denom


def set_voltage(port,voltage):
    '''Fonction qui permet de définir le output de tension sur un des ports analogiques out '''
    task = nidaqmx.Task()
    task.ao_channels.add_ao_voltage_chan(port,min_val=0,max_val=10.0) # Ajouter le canal analogique
    task.write(voltage)  # Écrire une tension sur le port


def mesure_v(port):
    '''Fonction qui permet de faire une lecture de voltage à une certaine fréquence sur le ports sélectionné '''

    task = nidaqmx.Task() # Coucou, wake-up
    task.ai_channels.add_ai_voltage_chan(
        physical_channel=port, min_val=0.0, max_val=2.0, units=VoltageUnits.VOLTS)  # initialise port
    task.timing.cfg_samp_clk_timing(sample_mode=AcquisitionType.FINITE)  # Spécification lecture MydaQ
    task.start()  # Commence à m'écouter
    v = task.read(number_of_samples_per_channel = 1)[0] # lit le port
    task.stop()#Ne m'écoute plus
    task.close() #Retourne dodo
    return v


def mesure_resistance(r1, vs, channel_list):
    '''Fonction qui permet de retourner la valeur de résistance d'une thermistance'''
    v0, v1 = mesure_v(channel_list[0]), mesure_v(channel_list[1])
    rt0 = r1*(1/((vs/v0)-1.0))
    rt1 = r1*(1/((vs/v1)-1.0))
    return rt0,rt1


def mesure_temperature(a,b,c, channel_list, freq):
    RT0, RT1 = mesure_resistance(115000.0,15.0, channel_list)
    T0 = 1/(a+(b*mt.log(RT0)) + (c*(mt.log(RT0))**3))
    T1 = 1/(a+(b*mt.log(RT1)) + (c*(mt.log(RT1))**3))
    print(f'Hot : {T0} °K,   Cold : {T1} °K')


class PowerControler:
    def __init__(self, port, p=0):
        self.port = port  # Port de l'élément chauffant
        self.power = p

    def set_power(self, p):
        self.power = p
        voltage = self.p_to_voltage(p)
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(self.port, min_val=0, max_val=10.0)  # Ajouter le canal analogique
            task.write(voltage)  # Écrire une tension sur le port

    @staticmethod
    def p_to_voltage(p):
        v = 0
        return v


if __name__ == "__main__":
    port = get_arduino_port()
    arduino = serial.Serial(port, baudrate=9600, timeout=0.2)
    arduino.close()
