import serial
import serial.tools.list_ports as list_ports
import numpy as np


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
    # Fonciton qui converti une valeur de tension en une valeur de température pour une thermistance
    arg = r * v / (e-v)
    denom = a + b * np.log(arg) + c * (np.log(arg))**3
    return 1 / denom


def measure_v(port):
    # Fonction qui va lire la tension sur un port du myDAQ
    mesure = 0
    return mesure


class PowerControler:
    def __init__(self, port, p=0):
        self.port = port  # Port de l'élément chauffant
        self.power = p

    def set_power(self, p):
        # Méthode pour fixer la valeur de la puissance à fourir
        pass


if __name__ == "__main__":
    port = get_arduino_port()
    arduino = serial.Serial(port, baudrate=9600, timeout=0.2)
    arduino.close()
