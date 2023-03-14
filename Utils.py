import serial
import serial.tools.list_ports as list_ports


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


port = get_arduino_port()
arduino = serial.Serial(port, baudrate=9600, timeout=0.2)
arduino.close()
